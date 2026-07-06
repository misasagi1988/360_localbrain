# 本脑版本SAE问题排查

标签（空格分隔）： SAE_DIAGNOSE

---

说明：这里主要针对本脑1.0及1.5版本。
wiki link: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22677529

## 1. 规则无法正常告警生成

### 1.1 需要现场提供的信息：

#### 1.1.1 基本信息

- 规则页面规则配置
- sae-core引擎加载的规则语句
- 满足条件的日志信息：在日志查询页面，根据规则配置的条件，找出满足条件的日志详细信息，信息尽量充足。
- sae-core.log：/opt/qihoo/soc/sae-core/logs/sae_core.log

#### 1.1.2 进阶信息

- incident日志：/opt/qihoo/soc/sae-core/logs/incident.log
- incident es日志：/opt/qihoo/soc/sae-core/logs/elasticsearch.log

### 1.2 排查思路

- 查看数据源配置，数据有没有发到kafka给sae消费
- 查看sae-core有没有正常加载规则。如果规则没有加载，可查看log，看sae在加载规则是否抛出异常。
- 查看sae-core日志是否有报错
- 查看日志是否存在问题
  - 日志的发生时间```occur_time```和接收时间```receive_time```影响了数据正常发出：当前，如果日志的发生时间早于接收时间2天，或晚于接收时间10分钟，dv不会发出该日志；
  - 日志中有解析错误，dv不会发出该日志；
  - 全局白名单影响：通过debug页面检查数据是否被全局白名单过滤。如果事件源地址、目的地址、域名、请求信息、用户账号、用户名称信息中任意一个字段与全局白名单匹配，则数据不进入引擎分析。全局白名单类型对应的检查字段如下：
  
    | 白名单类型 | 检查字段                                    |
    | ---------- | ------------------------------------------- |
    | IP         | 源地址(src_address)、目的地址(dst_address)  |
    | DOMAIN     | 域名(domain_name)                           |
    | URL        | 请求信息(request_msg)                       |
    | ACCOUNT    | 用户名称(user_name)、用户账号(user_account) |

- 消费告警数据：kafka消息保留时间有限制，时间靠前的数据，可能已丢失而消费不到。
  - 执行kafka命令消费告警topic，看下是否有告警生成。
    cmd: /opt/opt/qihoo/soc/kafka/bin/kafka-console-consumer.sh --bootstrap-server ${server_ip_port} --topic alarm -- from-beginning | grep ${alarm_name}， 如果存在，说明有生成告警，需要进一步排查incident的问题了。
  - 执行kafka命令消费日志topic，看下dv是否将数据输出到kafka。
    cmd: /opt/qihoo/soc/kafka/bin/kafka-console-consumer.sh --bootstrap-server ${server_ip_port} --topic hes-sae-group-0 -- from-beginning | grep ${event_id}，如果存在，说明日志有发到kafka。如果不存在，需要查看dv模块是否有问题。
- 执行历史任务
  - 如果消费不到告警数据，可新建历史任务，选择满足条件的一段时间内的日志做分析，看历史任务是否生成告警。如果历史任务有生成告警，说明是引擎问题，需要进一步排查问题原因。如果历史任务没有生成告警，则进一步检查数据是否满足条件或引擎是否存在问题。

## 2. 告警延迟，告警查询页面不连续，一段时间内没有或只有少量告警

### 2.1 需要现场提供的信息：

####  2.1.1 基本信息

- sae-core启动参数：ps aux|grep sae-core
- sae-core日志：/opt/qihoo/soc/sae-core/logs/sae_core.log
- sae-core metrics日志：/opt/qihoo/soc/sae-core/logs/metrics.log
- sae-core debug页面详细信息截图，引擎运行模式、kafka lag信息、以及各个节点的一系列状态监控信息，大部分信息需要打开metric开关方可获取。
- sae-core进程内各个线程的运行情况：top -H -p <pid>

### 2.2 排查思路

这种情况一般是由于数据量太大，sae-处理速度跟不上，或是个别规则处理速度慢，影响了sae整体的处理性能，导致有些数据还没有进入引擎做分析就被丢弃了。在sae-core的日志中应该也会看到大量"enqueue failed"的警告日志。debug页面，引擎的kafka lag应该会很大。

- 查看规则状态大小统计，定位innerWinSize多、subExpression多的规则，这些规则条件的数据很多，占用大量内存。可调大内存配置。
- 查看JVM Memory及JVM GC信息，如果内存占用率过高，GC频繁，可调大内存配置。
- 查看进程内各个线程的运行状态，找出高CPU的线程，进一步分析。一般运行过程中，esper数据处理类```DefaultMsgCb```相关线程cpu占用率较高，执行```jstack```命令，依据线程信息，进一步定位耗时高的操作。但当前无法定位具体规则，只能根据当前的规则状态、告警情况和规则配置情况做进一步猜测了。
- 查看规则耗时统计，根据cpuTime定位耗时大的规则。
- 查看UDF性能概要，定位耗时大的自定义函数和规则。







