# SAE引擎说明

标签（空格分隔）： SAE_DOC

---

- 引擎的架构
sae-monitor: 负责前端页面交互，规则增删改查，规则生成与db存储
sae-core: 负责实时流处理
- 数据处理流程
sae-core: source: kafka, destination: kafka
程序启动时，创建kafka consumer来消费kafka数据；创建第三方流处理分析引擎分析，加载db中的规则；创建引擎触发监听器，监听引擎响应数据，生成告警；创建AlarmProcesser，对告警数据进一步处理；创建kafka producer，将告警数据发出。
在数据处理时，通过构建多个生产者消费者模式，实现数据解耦和并发。
consumer读取数据后将数据放入阻塞队列A中；
单独线程从阻塞队列A中取数据，交给第三方流处理分析引擎分析；
告警数据放入阻塞队列B中；
AlarmProcesser从阻塞队列B中获取原始告警，做进一步处理，放入阻塞队列C；
producer从阻塞队列C中取数据，发出。
引入多个阻塞队列，以空间换时间，使得各个处理操作互不影响。
- 优化思路
consumer: 多线程消费数据
多线程创建多个分析引擎，分别加载不同规则，引入Disruptor框架，在多个生产者线程和多个消费者线程中传递数据，提升处理性能。
多线程处理告警数据
producer: 多线程发送数据
根据客户现场日志量，引入不同的分布式模式：
单机模式
分规则的分布式
分级的分布式：一级引擎做数据压缩降级和过滤；二级引擎消费一级引擎的压缩数据，生成告警


kafkaConsumer(5个线程，一个线程一个partition)->engine->triggerListener--放入阻塞队列LinkedBlockingQueue(20480)-->FurionProcess线程处理--放入阻塞队列LinkedBlockingQueue(20480)-->AlarmManager启动8个线程并行处理rawAlarm(主要是调用businessService服务加工告警数据，dispatcher服务将告警数据发出(kafka/inner/watchlist))


