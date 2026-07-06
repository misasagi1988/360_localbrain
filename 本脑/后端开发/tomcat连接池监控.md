标签（空格分隔）： 研发自驱 本脑v5.0版本后

---

### 需求说明

问题描述：
有人做复杂查询，tomcat连接hqlite的线程池被打满，web访问卡慢，metricbeat和tomcat连不通，最后ha把tomcat重启。 那么在连接数达到阈值的时候，是否增加告警监控呢？
优化方案：
对外提供服务的接口，线程连接池阈值增加告警，增加metricbeat上报信息，通过Monitor规则告警（monitor规则变更），增加日志打印

### 当前tomcat配置
来自server.xml
```
<Connector address="0.0.0.0" port="8080" protocol="HTTP/1.1" URIEncoding="UTF-8" maxHttpHeaderSize="102400" maxPostSize="-1"   //HTTP头最大100KB
               connectionTimeout="300000"   <!-- 连接超时5分钟 -->
               redirectPort="8443"
               maxParameterCount="1000"   <!-- 最大参数个数 -->
               />
```
这个配置中没有显式设置`maxThreads`，将使用默认值（通常200）

### 设计

#### tomcat作为服务提供者端监控

监控指标:

|指标类别   |指标名称       |说明       |
|---      |---      |---      |
|线程池       |maxThreads       |Tomcat最大线程数       |
|       |currentThreadCount       |当前线程总数       |
|       |currentThreadsBusy       |忙碌线程数       |
|连接       |connectionCount       |当前活跃连接数       |
|       |maxConnections       |最大连接数       |
|请求处理       |requestCount       |请求总数       |
|       |errorCount       |错误计数       |
|       |processingTime       |总处理时间       |
|       |avgPocessingTime       |平均处理时间       |
|JVM       |heap       |JVM堆内存使用情况       |
|JVM       |nonHeap       |JVM非堆内存使用情况       |

告警标准:

|指标|告警阈值|触发条件说明|
|---|---|---|
|`busyThreads`|> `maxThreads` * 0.9|tomcat连接池饱和，线程使用率超过90%持续2min|
|`currentThreads`|> `maxThreads` * 0.9|线程创建数接近最大值，ignore，暂时没用，保留数据|
|`connectionCount`|> `maxConnections` * 0.8|活跃连接数接近上限，ignore，暂时没用，保留数据|
|`avgProcessingTime`|> 3s|tomcat请求处理缓慢，平均响应时间变慢持续5min|
|`memoryUsedPercent`|> 0.9|内存使用率超过90%持续5min，ignore，暂时没用，保留数据|

### Q&A

metricbeat和tomcat连不通，那metricbeat送给monitor的tomcat相关的metric信息会带error，我们内置有tomcat运行状态异常监控规则，应该有告警的。页面哪边能看到？tomcat后台服务没有一个单独的页面展示。系统告警有什么提示？
我们的tomcat既可以对外提供web服务，在提供服务过程中也大量请求了hqlite，查询并获取数据。两种都需要做指标监控吧？
hqlite呢？作为对外提供服务的组件，是否也需要提供一些指标监控信息，制定监控告警策略，输出告警？
监控策略，持续时间配置有点问题，我们就是一个普通的follow-by规则，在时间间隔内满足即可触发


### 学习

#### tomcat连接池关注点
对于Tomcat作为对外提供HTTP接口服务的场景，涉及两种不同类型的连接池需要关注: 
1. 客户端连接池(HTTP连接池): 这是Tomcat处理外部HTTP请求时使用的连接池机制
关键组件: 
- **BIO/NIO连接器**：Tomcat用于接收HTTP请求的组件
- **线程池**：处理请求的工作线程池
连接被打满的表现: 
- 客户端收到`Connection refused`错误
- 请求响应时间显著增加
- Tomcat日志中出现"Max threads reached"警告
- 监控显示活跃线程数等于最大线程数
相关配置(server.xml): 
```
<Connector port="8080" protocol="HTTP/1.1"
           maxThreads="200"         <!-- 最大工作线程数 -->
           minSpareThreads="10"    <!-- 最小空闲线程 -->
           acceptCount="100"       <!-- 等待队列长度 -->
           maxConnections="10000" <!-- 最大同时连接数 -->
           connectionTimeout="20000"/>
```


2. 数据库连接池: 这是Tomcat应用访问数据库时使用的连接池。

#### 查看tomcat连接池状态
1. 系统命令
```
netstat -an | grep :8080 | awk '{print $6}' | sort | uniq -c
# 输出示例：
#   10 ESTABLISHED
#   5 TIME_WAIT
#   2 FIN_WAIT2
```
2. tomcat自带管理端
访问 `http://<host>:<port>/manager/status`（需要配置manager权限）

#### tomcat连接池被打满的表现
1. **客户端症状**：
    - 收到`Connection refused`或`502 Bad Gateway`
    - 请求响应时间曲线出现"悬崖式"上升
2. **服务端症状**：
    - 日志中出现大量"Max threads reached"警告
    - `Current thread busy`持续等于`maxThreads`
    - 监控图谱中`TIME_WAIT`状态连接激增