标签（空格分隔）： 本脑v4.0版本

---

本脑v4.0版本，参考[kafka核心参数统一配置](D:\\360本脑\\kafka\\Kafka重点参数调优.xmind)

# 需求说明

目前，本脑数据处理流都是通过kafka链路来实现的，各个模块的kafka producer&consumer参数配置都是放在各自的配置文件中的，并不统一。
之前就在客户现场出现过大的告警数据包无法发送到kafka的问题。
本需求的目的是，统一数据处理流中的kafka producer&consumer重点参数配置，将这些配置放在nacos的base.yml中，每个业务模块里引用公共配置的方式来实现。
只需要考虑核心数据处理链路即可。

# 涉及模块

- dv
    1. producer: 日志数据发到kafka，供其他模块消费
    2. consumer: 消费sae生成的内部事件，写入es
- sae
    1. consumer: 消费dv发出的日志数据，进行关联分析，触发告警；消费内部事件
    2. producer: 输出实时告警，历史任务生成的告警；内部事件
- angler
    1. producer: 输出实时告警，历史任务生成的告警 
- ice
    1. consumer: 消费实时告警，历史任务告警，ioc情报回扫告警，mdr上报上来的数据(`hql-filter-incident` topic，`hql-filter-merge` topic)
    2. producer:  发给soar的安全事件合并告警`incident-soar`，
- shuri
    1. consumer: 消费dv发出的日志数据，进行ioc情报匹配，生成威胁情报匹配事件
    2. producer: 输出ioc情报回扫告警
- artifacts
    1. consumer: 消费dv发出的日志数据，生成或更新实体消息；消费sae发出的告警数据，生成或更新实体消息；artifact-asset-integration，threat-graph-ti-result
    2. ~~producer: artifact-asset-compromise，incident-ioc~~
- tomcat人行数据上报，ConsumerService
    1. ~~consumer: 消费告警数据，感觉这部分不太合理：告警加白，告警字段调整，merge_key, 性能问题；~~
- 安装脚本，base.yml，kafka配置文件

tomcat人行数据上报，KafkaPublisherUtil，人行告警数据上报功能无需关注，只提取告警部分字段来上报。
告警数据外发功能无需关注，它的输入输出都不用kafka。

# 更新参数

producer：
```yaml
batch.size: 134217728
linger.ms: 1
compression.type: zstd
buffer.memory: 536870912
max.request.size: 1073741824
acks: all # 各模块自己控制
```
  
consumer：
```yaml
enable.auto.commit: true
session.timeout.ms: 30000
heartbeat.interval.ms: 10000
max.partition.fetch.bytes: 134217728
```

broker:
```yaml
message.max.bytes: 134217728
fetch.max.bytes: 134217728
```

# 各模块配置文件改动

kafka producer相关参数:
```yaml
compression.type: ${base.kafka.producer.compression.type}
linger.ms: ${base.kafka.producer.linger.ms}
batch.size: ${base.kafka.producer.batch.size}
buffer.memory: ${base.kafka.producer.buffer.memory}
max.request.size: ${base.kafka.producer.max.request.size}
```

kafka consumer相关参数：
```yaml
enable.auto.commit: ${base.kafka.consumer.enable.auto.commit}
session.timeout.ms: ${base.kafka.consumer.session.timeout.ms}
heartbeat.interval.ms: ${base.kafka.consumer.heartbeat.interval.ms}
max.partition.fetch.bytes: ${base.kafka.consumer.max.partition.fetch.bytes}
```