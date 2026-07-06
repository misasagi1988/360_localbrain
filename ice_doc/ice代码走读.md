# Incident代码走读

标签（空格分隔）： ICE_DESIGN

---

### 告警数据处理整理成一个处理链路
```
kafkaAlarmProcessChain：
// Alarm pre process，用data_source_array的值填充 data_source
// 更新ice引擎收到的最早告警开始时间，最晚结束时间，定时生成metrics，供monitor使用，默认告警最大延迟2h，monitor会触发警告
.startWith(new AlarmPreProcessNode())
// Alert doc transform，属性归一化，att&ck转集合，geo丰富化，提取内外网信息
.andThen(alarmTransformNode)
// Extract IOC from alarm，从告警中提取对应的ioc
.andThen(alarmExtractIocNode)
// ES bulk write，告警写入es，如果告警延迟超过1d，不进行后续处理
.andThen(alarmEsWriteNode)
// Handle default incident，合入已有(esper undateListener)或生成(esper unmatchedListener)默认安全事件，在创建安全事件的同时创建epl、合并告警并存入cache
.andThen(alarmDefaultIncidentProcessNode)
// Handle advanced incident，通过esper undateListener合入已有高级场景安全事件，ice规则引用了该告警规则，但没有生成安全事件的会创建对应安全事件，生成引擎epl，创建合并告警并存入cache
.andThen(alarmAdvancedIncidentProcessNode);
```
### rocksdb cache存放内容
```
epl: esper epl语句，key为安全事件id-编号，value是epl
incident: 存活的安全事件，key为安全事件id
alert_relation: 安全事件、合并告警、告警关系图，key为安全事件id-合并告警id-告警id，value为relation
log_relation: 安全事件、合并日志、日志关系图，key为安全事件id-合并日志id-日志id，value为relation
merge_alert: 存活的合并告警，key为merge_key
merge_event: 存活的合并日志，key为merge_key(安全事件id-年月日-事件名称)
search_task: 高级场景的搜索任务，key为

alert_relation_lookup
log_relation_lookup
merge_alert_lookup
merge_event_lookup
```
```xdr_update:
incident: 存活的安全事件，key为安全事件id
log_relation: log relation关系，key为安全事件id-合并日志id-日志id,
log_relation_lookup
merge_alert_new: 存活的合并告警，key为合并告警merge_key(日期-告警mergeKey)
merge_event: 存活的合并日志，key为合并日志merge_key(安全事件id-日期-事件名称)
merge_event_lookup: 先将数据堆积到内存buffer中，再异步定期刷新到rocksdb，以此来降低等待时间，提高吞吐量，目前log_relation及merge_event有这个
search_task: 级联的检索任务，重启ice时复原
xdr_update_rule: 后续告警关联的安全事件更新搜索epl，元素类型为XdrUpdateRuleItem，组成结构：安全事件id 编号 模型深度广度 搜索条件字节码，名称demo: 1636269400888619395 #010030 1-1 8389613b-306e-3128-8eb9-e7a79b0811f8
```
EngineEplCacheService
AsyncEplUpdateBuffer

SearchTaskPoolService: 用于执行ES搜索任务，可以有限降级，创建了两个线程池：
priorExecutor: 执行安全时间生成时的首次前向搜索，主要做告警查询，必须完成，10个线程，队列长度10000
weakExecutor: 执行一些递归搜索，主要做告警&日志查询，允许降级，10个线程，队列长度500
安全事件创建完毕后，关联的告警和日志的合入大都是通过es搜索来实现的，每个搜索会封装成一个SearchTask。

RecursiveSearchTaskManager
esAlarmProcessor
esEventProcessor


incident  log_relation  log_relation_lookup  merge_alert_new  merge_event  merge_event_lookup  search_task  xdr_update_rule



### 安全事件分数影响因素：

1. 安全事件severity：info: 1; warning: 25; critical: 50; fatal: 75;
2. 安全事件场景、关联的最高3个告警级别的告警的数量，分数最大值25
    EDR: 2.5*(top1*1.0+top2*0.2+top3*0.04)
    NDR/XDR: 0.25*(top1*1.0+top2*0.2+top3*0.04)
3. 安全事件相关的内网IP包含资产的分数，分数最大值100
4. 不同告警的总量，分数最大值100
5. 关联威胁情报(忽略)

评分 = 严重等级分数+ 告警级别个数评分 + (distinct告警名称评分 + 威胁情报评分 + 资产评分) / 300.0 * 25，最大值为100