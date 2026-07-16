# 共享基础设施模式实现方案

## Context

sae-monitor 与多个 sae-core 共用 Tomcat/DB/Redis/Nacos，只有一个 sae-monitor 实例。通过配置区分上下级 sae-core 节点。`globalRule=1` 的规则指定哪些节点加载完整规则，不加载的节点改为加载全局 EPL（filter OR 拼接）。

**关键改变**：不再走 ZK 注册和 Kafka 跨实例分发，规则直接存共享 DB。

---

## 1. 配置 + 配置类

### application.tpl.yml 末尾新增

```yaml
sae:
  cascade-mode: true
  node:
    current-node-id: sae-monitor-shared
    current-ccs-node-id: sae-monitor-ccs-shared
    upper-nodes: []
    lower-nodes: []
```

### 新建 `SaeNodeConfig`

**文件**：`src/main/java/com/hansight/hes/config/SaeNodeConfig.java`

```java
@Configuration
@ConfigurationProperties(prefix = "sae")
@Data
public class SaeNodeConfig {
    private boolean cascadeMode = true;
    private NodeProps node = new NodeProps();

    public boolean isSharedMode() { return !cascadeMode; }
    public List<String> getAllCoreNodes() {
        List<String> all = new ArrayList<>();
        if (node.getUpperNodes() != null) all.addAll(node.getUpperNodes());
        if (node.getLowerNodes() != null) all.addAll(node.getLowerNodes());
        return all;
    }

    @Data static class NodeProps {
        private String currentNodeId;
        private String currentCcsNodeId;
        private List<String> upperNodes = new ArrayList<>();
        private List<String> lowerNodes = new ArrayList<>();
    }
}
```

在 `CustomConfig` 中注册 bean。

**不需要** `sae.kafka.bootstrap-servers`，Kafka 地址从 `system_ccs_node` 表获取。

---

## 2. 启动流程改造

### `EntryPoint.initCurrentNode()`

**文件**：`src/main/java/com/hansight/hes/manager/EntryPoint.java`

注入 `SaeNodeConfig`。共享模式下用配置值，跳过 ZK 死循环：

```java
private void initCurrentNode() {
    if (saeNodeConfig.isSharedMode()) {
        GlobalSAEConstant.CURRENT_NODE_ID = saeNodeConfig.getNode().getCurrentNodeId();
        GlobalSAEConstant.CURRENT_CCS_NODE_ID = saeNodeConfig.getNode().getCurrentCcsNodeId();
        logger.info("shared mode, use config node id: {}", GlobalSAEConstant.CURRENT_NODE_ID);
        return;
    }
    // 原有 ZK 注册循环不变
}
```

---

## 3. 级联管理器 — 共享模式下 noop

四个管理器类各注入 `SaeNodeConfig`，在 `init()` 方法开头加判断：

| 文件 | 方法 |
|------|------|
| `node/ParentNodeManager.java` | `init()` |
| `node/ChildNodeManager.java` | `init()` |
| `distribute/ParentRuleDistributionManager.java` | `init()` |
| `distribute/ChildRuleDistributionManager.java` | `init()` |

```java
public void init() {
    if (saeNodeConfig.isSharedMode()) {
        logger.info("shared mode, skip init");
        return;
    }
    // 原有逻辑
}
```

**注意**：只在 `init()` 加判断即可。因为：
- `init()` 不执行 → `hasChild` 始终为 false → `update()`/`send()` 等方法的 `if (!hasChild) return;` 检查会自动拦截
- `AtomNodeNotificationHandler` 中调用的 `update()` 也会因为 `hasChild=false` 或找不到 parent 而提前 return

---

## 4. AtomNodeNotificationHandler

**文件**：`src/main/java/com/hansight/hes/notify/AtomNodeNotificationHandler.java`

共享模式下不监听节点注册/注销消息。在 `initConsumerCallBack()` 和 `initReloadCallBack()` 的回调中加判断：

```java
public void doConsume(String s) {
    if (saeNodeConfig.isSharedMode()) return true;  // 共享模式下不处理
    // 原有逻辑
}

public void doReload() {
    if (saeNodeConfig.isSharedMode()) return;  // 共享模式下不处理
    // 原有逻辑
}
```

---

## 5. RuleRawEntity 新增 globalRuleNodes 字段

**文件**：`src/main/java/com/hansight/hes/controller/entity/RuleRawEntity.java`

```java
/**
 * 全局关联分析指定加载规则的 sae-core 节点名称列表
 */
protected List<String> globalRuleNodes;
```

新增 getter/setter，更新 `toString()`。

**数据库存储**：
- **SAE 规则**（`sae_rule` 表）：新增 `global_rule_nodes` 列（JSON 字符串），在 RuleMapper.xml 中新增 resultMap 映射和 INSERT/UPDATE 映射
- **Mission 规则**（`search_rule` 表）：无需新增列，`globalRuleNodes` 已包含在 `raw` JSON 中，通过 `RuleRawTypeHandler` 自动序列化

---

## 6. MyBatis Mapper

### RuleMapper.java

**文件**：`src/main/java/com/hansight/hes/controller/dao/RuleMapper.java`

```java
List<Rule> findAllGlobalRules();
```

### RuleMapper.xml

**文件**：`src/main/resources/mapper/RuleMapper.xml`

- resultMap 新增 `global_rule_nodes` 列映射（存储为 JSON 字符串）
- INSERT/UPDATE 语句新增 `global_rule_nodes` 字段
- 新增 SQL：
```xml
<select id="findAllGlobalRules" resultMap="RuleResultMap">
    select * from sae_rule where status = 1 and global_rule = 1 and logic_delete = 0 ORDER BY id ASC
</select>
```

---

## 7. GlobalSAERuleService — 核心改动

**文件**：`src/main/java/com/hansight/hes/controller/service/GlobalSAERuleService.java`

注入 `SaeNodeConfig`。改造 `updateGlobalSaeRule()`：

```java
public void updateGlobalSaeRule() {
    if (saeNodeConfig.isSharedMode()) {
        updateGlobalSaeRuleSharedMode();
    } else {
        updateGlobalSaeRuleCascadeMode();  // 提取原有逻辑
    }
}

private void updateGlobalSaeRuleSharedMode() {
    List<Rule> allGlobalRules = ruleMapper.findAllGlobalRules();
    List<String> allCoreNodes = saeNodeConfig.getAllCoreNodes();

    Set<String> activeKeys = new HashSet<>();
    for (String nodeName : allCoreNodes) {
        // 排除该节点直接加载的规则
        List<Rule> filteredRules = allGlobalRules.stream()
            .filter(rule -> rule.getRaw() == null
                         || rule.getRaw().getGlobalRuleNodes() == null
                         || !rule.getRaw().getGlobalRuleNodes().contains(nodeName))
            .collect(Collectors.toList());

        String epl = Converter.buildGlobalSaeRule(filteredRules);
        String redisKey = GlobalSAEConstant.REDIS_GLOBAL_RULE_KEY_PREFIX + nodeName;
        activeKeys.add(redisKey);

        String origin = redisUtil.get(redisKey);
        if (!StringUtils.equalsIgnoreCase(origin, epl)) {
            if (epl != null) {
                redisUtil.set(redisKey, epl);
            } else {
                redisUtil.remove(redisKey);
            }
        }
    }

    // 清理已下线节点的 Redis key
    cleanupStaleRedisKeys(activeKeys);

    kafkaSdkProducerManager.sendMessage(MessageConstant.CHNL_SAE_MONITOR, MessageConstant.MSG_MONITOR_GLOBAL_RULE);
}

private void updateGlobalSaeRuleCascadeMode() {
    // 原有逻辑提取至此
    String origin = redisUtil.get(GlobalSAEConstant.REDIS_GLOBAL_RULE_KEY);
    List<Rule> rules = ruleMapper.findAllRunningParentRules();
    String current = Converter.buildGlobalSaeRule(rules);
    // ... 原有写入逻辑
}
```

### GlobalSAEConstant 新增

```java
public static final String REDIS_GLOBAL_RULE_KEY_PREFIX = "sae:global:rule:";
```

---

## 8. ExtraordinaryRuleService — 共享模式适配

**文件**：`src/main/java/com/hansight/hes/controller/service/ExtraordinaryRuleService.java`

注入 `SaeNodeConfig`。改造 `updateExtraordinaryRule()`：

```java
public void updateExtraordinaryRule() {
    if (saeNodeConfig.isSharedMode()) {
        updateExtraordinaryRuleSharedMode();
        return;
    }
    if (!saeCoreConfig.isClusterMode()) return;
    // 原有逻辑不变
}

private void updateExtraordinaryRuleSharedMode() {
    List<Rule> rules = ruleMapper.findAllRulesAggDisabled();
    for (String nodeName : saeNodeConfig.getAllCoreNodes()) {
        String epl = Converter.buildExtraordinaryRule(rules);
        String redisKey = DistributionRuleGramConstant.REDIS_EXTRAORDINARY_RULE_KEY_PREFIX + nodeName;
        String origin = redisUtil.get(redisKey);
        if (!StringUtils.equalsIgnoreCase(origin, epl)) {
            if (epl != null) redisUtil.set(redisKey, epl);
            else redisUtil.remove(redisKey);
        }
    }
    kafkaSdkProducerManager.sendMessage(MessageConstant.CHNL_SAE_MONITOR, MessageConstant.MSG_MONITOR_EXTRA_RULE);
}
```

### DistributionRuleGramConstant 新增

```java
public static final String REDIS_EXTRAORDINARY_RULE_KEY_PREFIX = "sae:distribution:rule:extraordinary:";
```

---

## 9. RuleService 触发全局 EPL 更新

**文件**：`src/main/java/com/hansight/hes/controller/service/RuleService.java`

在 `update()` 方法中，当规则的 `globalRule` 或 `globalRuleNodes` 变化时触发：

```java
// 在状态变更或规则内容变更后：
if (oldRule.getGlobalRule() != newRule.getGlobalRule()
    || !Objects.equals(oldRule.getRaw().getGlobalRuleNodes(), newRule.getRaw().getGlobalRuleNodes())) {
    globalSAERuleService.updateGlobalSaeRule();
}
```

在 `deleteSaeRule()` 方法末尾，删除成功后也调用一次。

---

## 10. RuleController API 适配

**文件**：`src/main/java/com/hansight/hes/controller/RuleController.java`

- `addSaeRule()` / `updateSaeRule()` 中，`globalRule=1` 时校验 `globalRuleNodes` 非空
- 新增 `GET /api/cep/sae-core-nodes` 返回 `SaeNodeConfig.getAllCoreNodes()`，供前端选择

---

## Redis key 变化

| 模式 | global EPL key | extraordinary EPL key |
|------|---------------|----------------------|
| 级联（现有） | `sae:global:rule` | `sae:distribution:rule:extraordinary` |
| 共享（新增） | `sae:global:rule:{nodeName}` × N | `sae:distribution:rule:extraordinary:{nodeName}` × N |

级联模式 key 保持不变，共享模式按节点拆分。

---

## 11. Mission（HQL 检索规则）适配

Mission 继承自 Rule，`SearchRuleRawEntity` 继承自 `RuleRawEntity`，`globalRule` 和 `globalRuleNodes` 字段天然可用。**但 `search_rule` 表没有独立的 `global_rule` 列，这些值存储在 `raw` JSON 中。** 需要适配以下三处：

### SearchRuleMapper.xml — 查询全局 Mission 规则

新增 SQL 从 JSON 中提取 `globalRule=1`：

```xml
<select id="findAllGlobalSearchRules" resultMap="RuleResultMap">
    select * from search_rule where status = 1 and logic_delete = 0
    and JSON_EXTRACT(raw, '$.globalRule') = 1
    ORDER BY id ASC
</select>
```

### GlobalSAERuleService — 合并 SAE + HQL 全局规则

在 `updateGlobalSaeRuleSharedMode()` 中，同时查询 SAE 和 Mission 的全局规则，合并后按节点过滤生成 EPL。

### RuleService.sendMessage() — HQL 分支增加节点过滤

**文件**：`src/main/java/com/hansight/hes/controller/service/RuleService.java`

当前 HQL 分支的 `sendMessage` 无条件发送消息，共享模式下需要加判断：

```java
case HQL:
    switch (action) {
        case ADD:
            if (isSearchRuleValidToCoreShared(ruleId)) {
                kafkaSdkProducerManager.sendMessage(... MSG_MONITOR_SEARCH_RULE ...);
            }
            break;
        // EDIT / DELETE 同理
    }
```

新增方法：
```java
private boolean isSearchRuleValidToCoreShared(String ruleId) {
    if (!saeNodeConfig.isSharedMode()) return true;  // 级联模式不变
    Mission mission = searchRuleMapper.findSearchRuleById(ruleId);
    if (mission == null) return false;
    if (mission.getGlobalRule() != 1) return true;  // 非全局规则，所有节点加载
    // 全局规则：检查 globalRuleNodes 是否为空（为空表示所有节点加载）
    List<String> nodes = mission.getRaw() != null ? mission.getRaw().getGlobalRuleNodes() : null;
    return nodes == null || nodes.isEmpty();
}
```

### RuleService.updateSearchRule() — 触发全局 EPL 更新

在 `updateSearchRule()` 方法中，当 `globalRule` 或 `globalRuleNodes` 变化时调用 `globalSAERuleService.updateGlobalSaeRule()`（与 SAE 规则同逻辑）。

---

## 实施顺序

| 阶段 | 步骤 | 原因 |
|------|------|------|
| 1 | SaeNodeConfig + application.tpl.yml | 基础配置 |
| 2 | EntryPoint | 启动流程改造 |
| 3 | 四个管理器 noop + AtomNodeNotificationHandler | 禁用级联逻辑 |
| 4 | RuleRawEntity + Mapper (SAE + HQL) | 数据模型 |
| 5 | GlobalSAERuleService + Converter 辅助 + 常量 | 全局 EPL 按节点生成 |
| 6 | ExtraordinaryRuleService 适配 | extraordinary rule 按节点存储 |
| 7 | RuleService (SAE + HQL 触发逻辑) + RuleController API | CRUD 闭环 |
| 8 | `./gradlew build -x test` 验证编译 |

---

## 向后兼容

- `sae.cascade-mode` 默认 `true`，无配置变更不受影响
- 所有改动通过 `isSharedMode()` 分支隔离
- Redis 新增 per-node key 不覆盖现有 key
- `nodeChain` 字段保留，共享模式下为空
- 数据库新增 `global_rule_nodes` 列（JSON 字符串），不破坏现有数据

---

## 验证

```bash
./gradlew build -x test
```

手动测试：
1. `cascade-mode: true` 启动 → 无回归
2. `cascade-mode: false` + 配置节点列表 → 日志确认管理器跳过、节点 ID 从配置读取
3. 创建 `globalRule=1` 规则，指定 `globalRuleNodes` → 检查 Redis `sae:global:rule:{nodeName}` 正确生成
4. 更新/删除规则 → Redis key 同步更新
