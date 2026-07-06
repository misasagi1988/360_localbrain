
### 分流原理

dcc中的数据接入进行源头分流至两个hes的topic。搭建两套sae处理集群，分别加载全部关联分析规则，并各自选择其中一个hes的topic进行处理，产生告警。
sae集群通过application.name做集群区分，不同sae集群，application.name不同。

### 分流改动

sae-monitor服务发现改动，发现多个不同application名称的sae服务。

### 分流逻辑问题

普通事件:
对于需要多个事件匹配触发的规则，可能由于不在同一个topic，导致规则无法触发，比如follow-by规则，A事件在topic-0，B事件在topic-1

内部事件相关:
新版本，内部事件发到单独topic，但所有sae都要消费该内部事件topic，对于使用内部事件的规则
事件源有一个且为内部事件，重复告警
事件源有多个且都为内部事件，重复告警

手动assign规则不适用，需改sae-core，及assgin规则接口，指定集群