# 本脑SAE全局关联分析

标签（空格分隔）： SAE_DESIGN

---

### 需求背景

多级节点部署情况下，针对一个规则，比如统计类规则，触发条件为having count(*) >=100，可能父节点收到了60条满足条件的数据，子节点收到了40条满足条件的数据，在这种情况下，也需要生成告警。但我们当前的环境是不支持的。应该说，除了普通模板类规则，其他类型的模板规则都存在这个问题。
后面我们需要支持这种场景。理论上多级支持无限级。

### 实现方案

- 多级节点之间的内网配置还有安全信息需保持一致（内网ip重复暂时不支持）
安全信息配置是比较容易保证一致的，但各个节点的内网配置可能是不相同的，这个暂时无法解决。

- 在SAE规则里添加“全局关联分析”的配置选项（普通模板不能配置）
  1. 在父节点配置之后由父节点统一下发到子节点，通过system_ccs_node表判断父子节点
  2. 父节点配置为“全局关联分析”的规则发往本节点kafka的固定topic，子节点的sae-monitor消费父节点发的topic数据，拿到规则信息
  3. 子节点对接收到的规则做处理（id+1000000，名称+‘_全局’），保存在mysql里，该规则在子节点只能显示，不能编辑和删除
  4. 父节点修改或删除规则之后同样发消息给子节点，子节点根据id+1000000做对应处理
  5. 父节点的注册与注销需要企业版通知到sae（目前好像已经有通知），如果注销了父节点，需要将所有的全局规则删除
目前已知晓：
注册及注销父节点时，会往redis的atom-node channel发消息
注册：REGISTERED
注销：UNREGISTERED
子节点可以通过监听这个channel获取父节点更新信息，如果存在父节点，可以读取system_ccs_node表拿到父节点的kafkaServer的具体信息。

### 具体实现
- sae-monitor
 - 规则变动：增加两个配置：本节点node_chain为null
    ```
    global_rule: int
    node_chain: string
    ```
 - 对规则的处理：
    1. 只允许编辑/删除/导出本节点规则。导出规则时只导出本节点创建的规则，全局使能开关置为disable。nodeChain置为null(其他节点导入时置为本节点nodeId)
    2. 子节点规则id+1000000，name+"_全局"，sysId置null，多级级联情况，id/name继续加，node_chain为生成规则节点的nodeId
    3. 只在sae规则配置页面更新规则时将规则的变动消息发给子节点
    4. 只将本节点规则变动消息发给sae-core
    5. 子节点将所有父节点规则的过滤条件做或拼接，形成大规则，给sae-core消费。过滤掉普通模板规则。
    规则变动消息，topic=qihoosoc-global-sae-rule，消息内容：
    ```
    rule_id:
    rule_name:
    action: add/edit/delete
    rule: rule raw entity
    ```
 - 节点变动消息(atom-node channel)处理：
    - 父节点
    ADD_CHILD: 创建kafka producer，发送规则，新增节点时将全部使能全局关联分析的规则发给子节点
    REMOVE_CHILD：check是否存在子节点，如果没有子节点，则删除kafka producer
    UPDATE_CHILD：do nothing
    - 子节点
    REGISTERED：创建kafka consumer，消费规则，存在孙节点，则将规则发往孙节点
    UNREGISTERED：删除kafka consumer，删除非本节点规则，删除redis全局关联分析大规则，存在孙节点，继续将规则删除消息发给孙节点

- sae-core
 - event
   topic: qihoosoc_sae_inner，事件携带node_chain_tag标识
   子节点将满足条件的数据发送到父节点kafka的特定topic，~~由父节点dv配置单独的数据源进行处理（dv需要添加对应的解析规则），父节点dv接收对应数据之后不写es，只做关联分析，告警溯源由es多集群来保证(交给dv的目的主要是为了适应sae集群部署时，多个一级engine消费不同topic的情况，由dv保证负载均衡)~~，当前topic定位内部事件topic(qihoosoc_sae_inner)，dv针对内部事件topic已经实现了上述功能，无需再重复实现同样的逻辑，发往内部事件topic即可
 - 规则处理
   1. 只加载本节点规则，全局关联分析大规则通过redis加载
   2. 单机/集群一级sae-core engine加载全局大规则，二级engine不加载，duplicate模式下0号sae-core engine加载全局大规则，其他不加载
   3. 全局关联分析大规则使用subscriber，通过kafka producer发给父节点
 - 节点变动消息
    - 父节点
    ADD_CHILD: 
    REMOVE_CHILD：
    UPDATE_CHILD：do nothing
    - 子节点
    REGISTERED：加载全局关联分析大规则，创建kafka producer，发送满足条件的数据
    UNREGISTERED：删除全局关联分析大规则，删除kafka producer
- node_chain:
 - 本节点规则node_chain为null，发送给子节点时携带好节点id信息，node_chain为创建该规则的节点id，子节点发送给孙节点时无效改动。
 - 规则导出时node_chain为null，只导出本节点规则，aggEnabled disable。

### attention

当前子节点页面不展示父节点用于全局关联分析的规则。在sae debug页面会展示。

### known issue

1. 父子节点属性配置有区别，有些字段可能子节点不存在，导致规则转换失败 ---ignore
2. 父子节点事件列表不一致，页面显示可能存在问题 ---ignore
3. 多级节点之间的内网配置还有安全信息需保持一致，安全信息配置是比较容易保证一致的，但各个节点的内网配置可能是不相同的，这个暂时无法解决。
4. 子节点上传数据需要时间，可能存在数据乱序导致父节点规则不生效问题

### 内部事输出逻辑改动：
节点运行模式：
 - 单机：
  - 内部事件直接交给engine
 - duplicate:
  - 内部事件发往hes-sae-group-0 topic
 - 分布式:
  - 内部事件轮询发往所有一级engine的topic
sae-core配置文件中指明当前运行模式及所有sae-core消费的topic

### 全局事件输出逻辑改动：
父节点运行模式：
 - 单机：
  - 全局事件发往hes-sae-group-0 topic
 - duplicate:
  - 全局事件发往hes-sae-group-0 topic
 - 分布式:
  - 全局事件轮询发往所有一级engine的topic
sae-core配置文件中指明父节点运行模式及所有sae-core消费的topic

### Q&A

1. 规则导入是否需要将全局使能的规则下发给子节点？目前不需要。规则导出时需要将全局使能开关disable。只在页面编辑时发送规则。
2. 子节点规则页面是否需要显示父节点规则？---yes
3. 历史任务是否允许使用父节点规则？---no
4. 有没有可能存在父子节点event id重复的情况？
5. 数据乱序
6. 统一系统时间 

所有子节点注销，父节点是否需要把所有全局关联分析disable?

### test

 - 前端测试功能点：
非本节点规则只允许查看，不允许用户编辑/删除/启停
历史任务只支持选用本节点规则

 - 后端测试功能点：
system_ccs_node数据表更新，增加kakfa_server字段，节点注册注销check

 - sae测试功能点：
sae-monitor:
规则：
全局使能规则变动信息下发子节点，子节点正常加载，id+1000000，name+"_全局"，sysId置null，多级级联情况，id/name继续加，node_chain为生成规则节点的nodeId。子节点更新全局关联分析大规则，给sae-core消费
只允许导出本节点规则，导出时全局使能disable，node_chain为null
节点变动：
注册：
父节点：可发送规则信息给子节点
子节点：接收父节点规则信息，页面正常展示
注销：
父节点不再发送规则信息
子节点删除所有非本节点规则
sae-core:
规则：
只加载本节点规则，全局关联分析大规则通过redis加载，名称为globalSAERule，发送满足条件的数据(携带本节点nodeID)给父节点，父节点能正常加载数据，生成告警
节点变动：
注册：
正常加载全局关联分析大规则，发送数据给父节点
注销：
删除全局关联分析大规则，停止发送数据给父节点

 - 测试时注意存在多个子节点及多级级联的情况。

### todo
本节点规则id不应该受影响

### 进一步优化思路
当前做法比较简单，子节点只起到过滤的作用，把满足条件的数据上报给父节点进行分析。但从现场实际情况来看，如果带宽较低，10Mb/s，以一笔数据1KB来算，1s大概1000条数据，如果子节点过滤不明显，可能有大量数据要传给父节点进行分析，会造成数据延迟。
进一步优化的思路：

 - 子节点可以先对数据做一下聚合，把聚合数据上传到父节点，这样数据量应该会小一些。
 - 子节点通过guava RateLimiter做流控，限制每秒发送给父节点的数据量






