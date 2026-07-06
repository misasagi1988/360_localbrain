# SAE问题排查

标签（空格分隔）： SAE_DIAGNOSE

---

## wiki

- 本脑1.0及1.5版本
  wiki link: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22677529
  本地: E:\Projects\sae\问题排查
- 企业版5.0版本、5.5版本及6.0版本 
  wiki link: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22677352
  本地: E:\Projects\sae\问题排查

## SAE常见问题及排查思路

### 1. 规则配置失败

#### 问题现象

添加或编辑sae规则，保存时页面提示错误，规则无法正常保存。

#### 排查思路

1. 确认规则配置是否正确
2. 查看sae-monitor log (log_path: /opt/qihoo/soc/tomcat/logs/sae_monitor.log)，是否出现异常，一般属性类型不识别或属性类型使用错误会导致规则生成失败。
   - demo-1，user_account属性不识别。这种情况下需求检查system_attribute属性表中是否存在该字段且该字段是否属于事件(type&1=1)或告警(type&2=2)SIM模型，如果不是，更新属性表该字段的type值，重启tomcat及sae-core。  

```java
SELECT * FROM GlobalEvent(`event_name`='A' and `user_account` = 'B') AS A
     2021-03-29 14:21:07,877:INFO main (c.e.e.c.s.StatementLifecycleSvcImpl:1056) - Failed to compile statement: Failed to validate filter expression 'event_name="A" and user_account="B"': Property named 'user_account' is not valid in any stream
     com.espertech.esper.epl.expression.core.ExprValidationException: Failed to validate filter expression 'event_name="A" and user_account="B"': Property named 'user_account' is not valid in any stream
     	at com.espertech.esper.epl.expression.core.ExprNodeUtility.getValidatedSubtree(ExprNodeUtility.java:331) ~[esper-6.1.0-optimized.jar:?]
```
   - demo-2, target_process_id为string类型，source_process_id为整形，A.source_process_id = B.target_process_id，属性类型不兼容，导致规则转换失败。这种情况属于规则配置错误，需要修改规则。
   
 ```java
SELECT  A.`src_address` , B.`src_address`  FROM PATTERN[EVERY A=GlobalEvent(event_name='A')->(B=GlobalEvent(event_name='B' and A.source_process_id = B.target_process_id) WHERE timer:within(20 min)) WHILE (A.occur_time <=B.occur_time AND B.occur_time - A.occur_time <=600000) ]
     2021-03-29 14:48:48,103:INFO main (c.e.e.c.s.StatementLifecycleSvcImpl:1056) - Failed to compile statement: Failed to validate filter expression 'event_name="B" and A.source_process...(58 chars)': Implicit conversion from datatype 'String' to 'Long' is not allowed
     com.espertech.esper.epl.expression.core.ExprValidationException: Failed to validate filter expression 'event_name="B" and A.source_process...(58 chars)': Implicit conversion from datatype 'String' to 'Long' is not allowed
    	at com.espertech.esper.epl.expression.core.ExprNodeUtility.getValidatedSubtree(ExprNodeUtility.java:331) ~[esper-6.1.0-optimized.jar:?]
 ```


### 2. 告警无法正常生成

#### 问题现象

日志页面可查到满足条件的日志，但没有告警生成。

#### 可能影响因素

1. dv数据源配置有问题，数据存储没有选择Enterprise-SAE-KAFKA
2. 日志有问题，dv没有将日志发到进行分析  
   - 日志解析错误，dv解析类型不对；
   - 日志的发生时间偏移过大，发生时间```occur_time```和接收时间```receive_time```影响了数据正常发出：当前，如果日志的发生时间早于接收时间2天，或晚于接收时间10分钟，dv不会发出该日志：解析错误字段 包含 time offset
   - 日志中有解析错误，缺少关键字段(不是所有的解析错误都不发kafka)；
   - 全局白名单影响：查看事件的```src_address、dst_address、domain_name、request_msg、user_name、user_account```这几个字段是否位于全局白名单中，全局白名单中的数据不进入引擎分析。
3. 新增或修改过信息组、内网、白名单等信息  
   如果规则有引用这些信息，而这些信息在日志时间范围内有变动，则可能导致过滤条件不满足而无法正常生成告警。

#### 排查思路

a. 所有告警都不生成
1. 查看sae-core consumer消费kafka数据的状态，看sae-core消费是否正常  
   cmd:  ```/opt/qihoo/soc/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group qihoosoc-sae```
2. 查看sae-core的metrics日志(log_path: /opt/qihoo/soc/sae-core/logs/metrics.log)，看是否有日志消费和告警输出。log format: 

   2021-03-29 15:17:18,174:INFO metrics-logger-reporter-1-thread-1 - metrics info:
    name=aggregationEvent, total_count=[0], period_count=[0], eps=[0]
    name=aggregationOutput, total_count=[0], period_count=[0], eps=[0]
    name=alarm_analyzed, total_count=[1350], period_count=[0], eps=[0]
    name=alarm_sent, total_count=[1350], period_count=[0], eps=[0]
    name=inner_event, total_count=[309], period_count=[0], eps=[0]
    name=kafka_consumer_hes-sae-group-0, total_count=[1634], period_count=[0], eps=[0]
    name=logEvent, total_count=[1634], period_count=[0], eps=[0]
    name=saeAlarm, total_count=[1350], period_count=[0], eps=[0]
    name=alarm_manager_queue, current_number=[0]
    name=inner_alarm_queue, current_number=[0] 
    
    logEvent为接收日志的统计信息，alarm_sent为生成告警的统计信息。

3. 消费下kafka的告警数据，区分是sae的问题还是ice的问题，如果有正常输出告警，但页面查不到，可查看是否是ice写入告警失败  
   cmd:  ```/opt/qihoo/soc/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic alarm --from-beginning```

b. 个别规则告警不生成

1. 查看debug页面，看sae是否正常加载该规则；  
   1) 访问DEBUG页面：https://172.16.100.225/PC090MFF0009/cep/debug  
   2) 点击sae引擎节点，进入sae引擎DEBUG页面  
   3) 在所有生效规则中，输入规则名称进行搜索，看该规则是否存在且运行规则epl内容非空。  
   如果搜索不到该规则或运行规则为空，则规则没有被正常加载。这时，需要查一下sae-core.log，看下规则加载是否有异常。Exception demo：c_attr_demo字段不识别，导致规则加载失败:

      ```
   2021-03-29 16:09:01,989:ERROR main (EngineCore.java:279) - add rule to realtime engine failed: 
   com.espertech.esper.client.EPStatementException: Error starting statement: Failed to validate select-clause expression 'A.c_attr_demo': Failed to resolve property 'A.c_attr_demo' to a stream or nested property in a stream [SELECT A.`occur_time` AS `start_time`, A.`occur_time` AS `end_time`, A.`net_protocol` AS `net_protocol`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, A.`vulnerability_id` AS `vulnerability_id`, A.`c_attr_demo` AS `c_attr_demo`, id, data_source, client_host_sign, attack_id, ti_dimension, event_id, data_source_array, client_host_sign_array, attack_id_array  FROM GlobalEvent(node_chain_tag is null AND (event_name='ssh连接')) AS A]
      ```
   这种情况下需要检查属性表是否存在这个字段及这个字段的类型。
2. 执行历史任务，看能否正常生成告警，执行时注意添加过滤条件，尽快完成历史任务；
3. 消费下kafka的日志数据，确认dv是否将数据发出  
   cmd:  ```/opt/qihoo/soc/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic hes-sae-group-0 --from-beginning```
4. 消费下kafka的告警数据，区分是sae的问题还是ice的问题，如果有正常输出告警，但页面查不到，可查看是否是ice写入告警失败；
5. 查看sae-core.log，看是否有消费异常。sae-core处理逻辑是读取日志数据后将其放入队列中依次处理的，如果数据量较大，队列放不下，则会出现数据无法进入引擎分析即丢失的情况，导致告警漏报。log format: ```enqueue failed, queue size:... ```；
6. 查看sae-core.log，看告警处理是否存在问题。如果告警无效或在后续处理时抛异常，会导致告警丢弃。如果告警没有开始时间及结束时间字段，或开始时间大于结束时间，则是一个无效的告警，log format: ```illegal alarm data:... ```；
7. 规则known issue：follow-by规则涉及3个及以上事件时，可能会有告警漏报；not before模板的规则，第一个告警可能会生成不了。

### 3. sae处理速度慢，kafka lag很大

#### 问题现象

sae ep较低，kafka lag很大，达到百万级别。

#### 可能影响因素
1. 日志量有显著增加
2. 有新增或者修改关联分析规则
3. 个别规则处理速度慢，影响了整体的处理性能

#### 排查思路

1. 查看日志查询页面，展开趋势统计，看日志是否有显著增加。如果日志陡增，sae-core一时处理不过来，可能会造成告警延迟；
2. 从客户现场实际运行来看，```rlike、belong```操作符耗时较长；规则分组数量多，时间窗口设置较长，大量数据进入时间窗口，会导致较高的内存占用。可进入sae-core DEBUG页面，打开metric开关，查看“**规则状态监控**”、“**UDF性能概要**”、“**规则状态大小统计**”，查看规则状态及自定义函数耗时，定位耗时大的规则、窗口数据量多的规则及处理速度慢的自定义函数；
3. ```top```命令，查看sae-core进程信息，定位高CPU线程。一般运行过程中，esper数据处理类```DefaultMsgCb```相关线程cpu占用率较高，执行```jstack```命令，依据线程信息，进一步定位耗时高的操作。但当前无法定位具体规则，只能根据当前的规则状态、告警情况和规则配置情况做进一步猜测了，尝试将某些规则的```rlike```条件改为信息组实现，优化规则过滤条件顺序，进一步观察topic lag情况。

## 附录一

### 1. SAE可用的debug接口

/api/cep/core/utils/intelligence, get(id), 获取该id情报组的具体内容  
/api/cep/core/utils/intelligence/query, get(ig, type, group), check特征内容是否属于特征，ig为内容，type为特征类型  (string/num/ip/full_regex/half_regex/time)，group为特征信息。ex: /api/cep/core/utils/intelligence/query?ig=127.0.0.1&type=ip&group=CSWLHT4101a6，判断127.0.0.1是否为内网IP  
/api/cep/core/utils/asset/query, get(ip)，check 该ip是否属于资产  
/api/cep/core/utils/whitelist/query, get(value, type)，check该类型(ip/domain/url/account)的全局白名单是否存在  
/api/cep/core/utils/reload/rules, post, 重新加载所有规则  
/api/cep/core/utils/reload/intelligence, post, 重新加载所有安全信息  
/api/cep/core/utils/reload/asset, post, 重新加载所有资产信息  
/api/cep/core/utils/reload/whitelist, post, 重新加载所有全局白名单  
/api/cep/core/utils/reload/all, post, 重新加载以上所有  

### 2. 常见kafka命令

kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list, 列出当前kafka的所有topic  
kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group qihoosoc-sae, 列出当前qihoosoc-sae消费组的消费状态  
kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic hes-sae-group-0 --from-beginning , 从头消费hes-sae-group-0 topic的数据  

## 附录二

### 1. SAE规则配置说明

##### 事件源说明

可以配置事件源为全局事件或具体事件，全局事件需配置过滤条件。


##### 规则模板说明

当前SAE规则共有十一个模板，具体说明如下:

| 模板名称                        | 模板描述                                                     | 事件源配置         |
| ------------------------------- | ------------------------------------------------------------ | ------------------ |
| 普通模板                        | 基于单个事件的触发，一对一告警。                             | 有且只有一个事件源 |
| 普通模板-having count(DISTINCT) | 在一段时间内，连续多次事件中某个属性出现不同的次数符合条件即触发告警，统计类告警。 | 有且只有一个事件源 |
| 普通模板-having count(*)        | 在一段时间内，某事件发生的次数符合条件即触发告警，统计类告警。 | 有且只有一个事件源 |
| 普通模板-having sum             | 在一段时间内，多次事件中某属性值的和符合条件即触发告警，统计类告警。 | 有且只有一个事件源 |
| 关联模板-follow_by              | 某事件A之后的一段时间内发生了事件B，关联类告警。             | 至少两个事件源     |
| 关联模板-not_follow_by          | 某事件A之后的一段时间内一定不发生事件B，关联类告警。         | 有且只有两个事件源 |
| 关联模板-or_follow_by           | 在一段时间内，事件A和事件B均发生，但无发生时间先后要求，普通告警。 | 有且只有两个事件源 |
| 关联模板-not_before             | 事件B发生之前的一段时间内没有发生事件A，当前关联条件只支持多个与逻辑运算，关联类告警。 | 有且只有两个事件源 |
| 关联模板-Repeat-Until           | 至少M次事件A发生之后的一段时间内发生了事件B，关联类告警。规则可配置关联条件，AB的关联字段数量必须一致。 | 有且只有两个事件源 |
| 关联模板-No-Order               | 一段时间内发生多个事件，发生时间无顺序要求，关联类告警。规则不允许配置关联条件，可配置分组条件。 | 至少两个事件源     |
| 普通模板-not occur              | 一段时间内某事件A没有发生。                                  | 有且只有一个事件源 |

##### 操作符说明

当前支持的操作符有```=/!=/>/>=/</<=/exist/not_exist/like/rlike/in/belong/contain/match/inmap/not_inmap```，右操作数既支持手动输入，也支持选择特定选项。由于前端没有根据左操作数类型对其允许的操作符加以限制，配置的时候需要特别注意。

1.  =/!=/>/>=/</<=: 关系操作符
2.  exist/not_exist: 存在/不存在，无右操作数
3.  字符串匹配类操作符，针对特殊字符需要特别处理。其中，  
    like: 字符串匹配，部分匹配即可，忽略大小写，支持字符串数组(数组任意元素like即可)  
    rlike: 正则匹配，全匹配，忽略大小写
4.  in: 针对ip类型，属于网段；如果输入值以[开头以]结尾，则右值表示数组，用于判断左值是否包含在右值表示的数组中
5.  belong: 属于特征，针对系统内置安全信息，右操作数仅支持F配置
6.  contain: 关联包含，针对list和数组类型
7.  match: 匹配情报，无右操作数，当前仅针对源地址/目的地址/域名三个字段有效。在配置威胁情报相关的规则时注意事件源名称更新为威胁情报IP匹配事件或威胁情报Domain匹配事件。
8.  inmap: 针对多维信息组，多维信息组的key和value仅支持单个值，不支持区间格式。demo: 源地址 inmap 多维信息组测试.目的地址，目的地址是多维信息组的键，且源地址在目的地址对应多维信息组键的值的set里。key，value 都匹配。
9.  not_inmap: 针对多维信息组，多维信息组的key和value仅支持单个值，不支持区间格式。demo: 源地址 not_inmap 多维信息组测试.目的地址，目的地址是多维信息组的键，且源地址不在目的地址对应多维信息组键的值的set里。key匹配，value不匹配。









