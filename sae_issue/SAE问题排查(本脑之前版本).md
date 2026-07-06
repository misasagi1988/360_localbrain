# SAE问题排查(本脑之前版本)

标签（空格分隔）： SAE_DIAGNOSE

---

说明：这里主要针对企业版5.0版本、5.5版本及6.0版本。
wiki link: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22677352

## 常见问题及排查思路

### 1. 规则无法正常告警生成

#### 1.1 需要现场提供的信息：

##### 1.1.1 基本信息

- 规则配置信息
  - 页面规则配置
  - 连接mysql hansight数据库，执行sql命令：select id, rule_name, statement, alarm_attr from sae_rule where rule_name='${rule_name}' and status > 0；//${rule_name}换为具体的规则名称；
- sae-core引擎规则加载情况
  - 连接后台sae-core，发送请求并导出到文件：curl "http://127.0.0.1:8765/api/cep/debug/epl" > epl.log，打开epl.log，根据规则名称搜索sae-core加载的对应规则语句；
- 满足条件的日志信息：在日志查询页面，根据规则配置的条件，找出满足条件的日志详细信息，信息尽量充足。事件中，事件名称和id必须存在，事件分类不能为"/other/other"。
- sae-core.log：/opt/hansight/enterprise/sae-core/logs/sae_core.log

##### 1.1.2 进阶信息

- 环境全局白名单配置
- incident日志：/opt/hansight/enterprise/incident/logs/incident.log
- incident es日志：/opt/hansight/enterprise/incident/logs/elasticsearch.log

#### 1.2 排查思路

- 查看数据源配置，数据有没有发到kafka给sae消费
- 查看sae-core有没有正常加载规则
- 调用接口，看sae有没有正常加载规则信息。如果规则没有加载，可查看log，看sae在加载规则是否抛出异常。
- 查看sae-core日志是否有报错
  - 确认下sae-core在处理数据时是否抛异常。如果数据的字段类型与环境属性类型不匹配，则sae-core在处理时会抛异常，需查看解析规则是否有问题。
  - 常见异常一：com.espertech.esper.client.EPException: java.lang.ClassCastException: java.lang.String cannot be cast to java.lang.Number，字段为整形，事件中是字符串类型。
  - 常见异常二：java.lang.IllegalArgumentException: array element type mismatch，这个问题是统计类规则聚合时某个字段的值类型不一致导致的。
- 检查数据是否被全局白名单过滤
  - 如果事件源地址、目的地址、域名、请求信息、用户账号、用户名称信息中任意一个字段与全局白名单匹配，则数据不进入引擎分析。全局白名单类型对应的检查字段如下：
  
    | 白名单类型 | 检查字段                                    |
    | ---------- | ------------------------------------------- |
    | IP         | 源地址(src_address)、目的地址(dst_address)  |
    | DOMAIN     | 域名(domain_name)                           |
    | URL        | 请求信息(request_msg)                       |
    | ACCOUNT    | 用户名称(user_name)、用户账号(user_account) |

- 消费告警数据：kafka消息保留时间有限制，时间靠前的数据，可能已丢失而消费不到。
  - 执行kafka命令消费告警topic，看下是否有告警生成。
    cmd: /opt/hansight/enterprise/kafka/bin/kafka-console-consumer.sh --bootstrap-server ${server_ip_port} --topic alarm -- from-beginning | grep ${alarm_name}， 如果存在，说明有生成告警，需要进一步排查incident的问题了。
  - 执行kafka命令消费日志topic，看下dv是否将数据输出到kafka。
    cmd: /opt/hansight/enterprise/kafka/bin/kafka-console-consumer.sh --bootstrap-server ${server_ip_port} --topic hes-sae-group-x -- from-beginning | grep ${event_id}，如果存在，说明日志有发到kafka。如果不存在，需要查看dv模块是否有问题。x为事件所在分组。
- 执行历史任务
  - 如果消费不到告警数据，可新建历史任务，选择满足条件的一段时间内的日志做分析，看历史任务是否生成告警。如果历史任务有生成告警，说明是引擎问题，需要进一步排查问题原因。如果历史任务没有生成告警，则进一步检查数据是否满足条件或引擎是否存在问题。

### 2. 告警延迟，告警查询页面不连续，一段时间内没有或只有少量告警

#### 2.1 需要现场提供的信息：

#####  2.1.1 基本信息

- sae-monitor配置文件：/opt/hansight/enterprise/tomcat/webapps/sae/WEB-INF/classes/application.yml，搜索server配置，cluster为false表示环境是单机部署，为true表示环境是集群模式。
- sae-core配置文件：/opt/hansight/enterprise/sae-core/application.yml，搜索balance和engine配置，截图
- sae-core启动参数：ps aux|grep sae-core
- sae-core日志：/opt/hansight/enterprise/sae-core/logs/sae_core.log
- sae-core metrics日志：/opt/hansight/enterprise/sae-core/logs/metrics.log
- kafka lag情况：/opt/hansight/enterprise/kafka/bin/kafka-consumer-groups.sh --bootstrap-server ${server_ip_port} -describe --group hansight-sae 

##### 2.1.2 进阶信息

- sae-core进程GC信息：jstat -gccause sae-pid 3000 10，定时采样10次进程GC信息
- sae-core规则metrics信息，发送请求并导出到文件：curl "http://127.0.0.1:8765/api/cep/debug/metrics/statement" >metrics.log。
- sae-core进程内各个线程的运行情况：top -H -p <pid>

#### 2.2 排查思路

这种情况一般是由于数据量太大，sae-处理速度跟不上，或是个别规则处理速度慢，影响了sae整体的处理性能，导致有些数据还没有进入引擎做分析就被丢弃了。在sae-core的日志中应该也会看到大量"enqueue failed"的警告日志。查看kafka lag，lag应该会很大。

- 查看日志查询页面，展开趋势统计，看日志是否有显著增加。如果日志陡增，sae-core一时处理不过来，可能会造成告警延迟；
- 如果GC异常，频繁Full GC，GC耗时大，可调大sae-core内存配置。如果规则分组数量多，时间窗口设置较长，时间窗口内缓存了大量的数据，会导致较高的内存占用。
- 如果GC正常，应该是环境中配置的有些规则耗时较大，拖慢了引擎的处理速度，需要进一步定位下环境中的慢规则。
  - 查看进程内各个线程的运行状态，找出高CPU的线程，进一步分析。一般运行过程中，esper数据处理类```DefaultMsgCb```相关线程cpu占用率较高，执行```jstack```命令，依据线程信息，进一步定位耗时高的操作。但当前无法定位具体规则，只能根据当前的规则状态、告警情况和规则配置情况做进一步猜测了。
  - 打开规则metrics配置(如果sae-core配置文件的engine.metric_on为false，需改为true后重启sae-core)，请求规则metrics信息，获取cpuTime较大的规则。
  - 根据经验，rlike和belong正则类信息组处理速度比较慢，可以查询数据表，获取所有使用了rlike和belong操作符的规则，进一步分析，查询sql语句：select id, rule_name from sae_rule where (raw like "% rlike %" or raw like " belong ") and status > 0。尝试将优化规则过滤条件顺序和语句，调整时间窗口配置，进一步观察topic lag情况。
- 如果环境是集群部署的，可调用接口查看是否有topic没有被消费，尝试调大引擎的balance.ability配置以消费到topic。接口：curl "http://127.0.0.1:8765/api/cep/core/utils/topic/ignored"

### 3. 引擎重启

在设计时，为了保证引擎的正常运行，我们会在运行期间定时检查引擎单位时间的内存占用率、cpu占用率和Full GC次数，如果连续多次内存占用率过高并且Full GC次数过于频繁，就会触发引擎重启。日志中会看到"service will exit in 5 sec for illegal memory state"。这种情况下建议调大内存配置，定位并优化慢规则。如果环境为单机模式，可尝试改为集群模式。






