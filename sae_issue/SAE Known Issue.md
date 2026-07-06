# SAE Known Issue

标签（空格分隔）： SAE_ISSUE

---

### follow-by模板规则，涉及三个及以上事件时，可能会有告警漏报。
原因分析：当前规则epl语句生成时，会将关联条件放到最后一个事件中作为过滤条件，并没有将其进一步拆分，这样可能导致不满足条件的中间事件放入pattern，影响告警生成。

### Repeat_until模板规则未正确生成告警

参考bug ID1005060。
针对repeat-until模板规则，sae的epl采用的是esper的repeat逻辑实现，A可以重复多次，通过where timer:within限定时间窗口，while条件检查时间是否满足要求。
处理时，会把每批match count的A缓存，直到B过来。如果第一批A数据已经生成了，但第二批A还没达到计数，那只会检查B和第一批数据A[0]的发生时间差是否满足时间窗口长度要求，如果不满足则无法正常生成告警。

### not before--内部事件的规则，第一个告警可能会生成不了

程序启动后，规则会读取所有事件，记录当前已观察到的最小事件时间赋值给activeTime，作为证据，证明在该时刻之后的事件理论上都已经读取过（无乱序的情况下）。如果新事件的 lastA == null && eventTime - within < activeTime （检测周期内没有检测到A），则该事件B之前未必不存在事件A, 仅仅是启动后的这段时间内kafka没有输出过事件A（可能在上次启动周期内输出过），因此此时不会触发告警。
这样做主要是为了防止误报，我们并不清楚程序重启之前es里面数据的情况，如果规则时间窗口设置较长，可能会有误报。

### any-order模板，只支持配置分组条件，不支持配置其中某几个事件的、不同字段的关联条件。

### not-before模板: 关联条件只适合and逻辑和=操作符 

### 统计类规则，输出字段值取最后一个事件的字段值

这可能导致一个问题，两个告警的数据内容是完全一样的，只是事件先后顺序不同，导致生成告警的direction_key不同，如果使用ice默认策略，会生成两个安全事件，无法跟客户解释。

### 规则启用动态信息，执行历史任务时，会影响实时数据匹配

### sae内容包规则问题分类

统计类规则，触发条件>=1
未启用告警及内部事件，导致规则无效
过滤条件、关联条件理解错误，在关联条件中配置某一事件的过滤条件
内部事件与普通事件重名
内部事件名称不合适(建议以"内部事件-"开头)
普通模板生成内部事件
规则引用事件不存在
内部事件没有被任何规则使用
内部事件输出字段不完整，引用内部事件的规则无效
规则过滤条件/关联条件中使用的事件的字段不在事件所属sim模型内，导致页面显示有问题

### 统计类规则，window event_id聚合数量check

~~### 事件名称不存在时，导入SAE规则报错
当前规则导入的处理逻辑是这样的：
如果规则导入失败，会循环尝试重复n次，n=failCount*100，直到规则全部导入成功方break。这个逻辑存在问题，目前还没有想到更好的方法，暂时先这样。
***导入逻辑已修改，该问题不存在。***~~

~~### SAE内部事件名称check，不允许与事件源重名，否则可能会导致陷入死循环
关联分析规则里只是按事件名称生成告警的，而勾选了内部事件，且内部事件跟原事件名称一样
***问题已解决***~~


### Not occur模板设计思路
Qradar实现思路:
QRadar uses a watcher task that periodically queries the last time that an event was seen (last seen time), and stores this time for the
event, for each log source. The rule is triggered when the difference between this last seen time and the current time exceeds the number of seconds that is configured in the rule.

 - 方案1：
记录last A的occur_time，记为a_occur_time，及当前日志时间的最大值max，记为max_occur_time。类似qradar，使用定时任务，周期性的检查max_occur_time与a_occur_time时间差是否超过设置的时间窗口长度，如果超过，则告警，定时任务执行周期为时间窗口长度。
优点：不会有告警误报
缺点：需要使用timer task，检查逻辑在定时任务中实现，较为复杂；可能会有告警延迟。

 - 方案2：
同样，记录last A的occur_time，记为a_occur_time，及当前日志时间的最大值max，记为max_occur_time。但不使用定时任务，而是交由自定义函数来检查max_occur_time与a_occur_time时间差是否超过设置的时间窗口长度，如果超过，则告警。
优点：相比方案1更容易一些
缺点：需要额外增加判断逻辑，防止重复告警；事件驱动，如果环境没有日志过来，则无告警

 - 方案3：
esper的pattern语法，timer:interval
优点：简单
缺点：没有采用日志时间，可能会因日志延迟导致告警误报

 - 方案4：
搜索告警
优点：简单，基本不动代码(不过当前代码有点问题，</<=/=操作符的时候不应该用subMissionService)
缺点：belong 信息组会有问题

告警限制：超过时间窗口长度，只生成一次告警还是重复生成？
告警字段：id, start_time, end_time, alarm related attrs


