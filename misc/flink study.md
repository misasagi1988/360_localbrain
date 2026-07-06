# Flink Study

标签（空格分隔）： 未分类

---
### flink简介
事件驱动的，分布式数据处理引擎，用于对有界和无界的数据流做有状态的计算。
流式数据: 一个一个连续不断生成的
流处理目标: 高吞吐，低延迟，结果准确，良好的容错性。
支持事件时间和处理时间。

### flink运行组件
JobManager
TaskManager
ResourceManager
Dispatcher

开发步骤:
Environment -> Source -> Transform -> Sink
environment负责创建执行环境
source负责读取数据源
transform负责利用各种算子进行加工处理
sink负责输出

窗口类型：
 - 时间窗口：滑动Sliding/滚动Tumbling，基于事件时间/进入Flink处理的时间。滑动窗口由固定的时间窗口长度和滑动间隔组成，窗口长度固定，可以有重叠
 - 计数窗口：滑动/滚动
 - 会话窗口：基于时间
窗口函数~


事件时间
水位线waterMark：数据可能有延迟，设置水位线来企图让数据更加准确

检查点checkPoint：Flink会在指定的时间段上保存状态的信息，假设Flink挂了可以将上一次状态信息再捞出来，重放还没保存的数据来执行计算，最终实现exactly once。Flink在流处理过程中插入了barrier，每个环节处理到barrier都会上报，等到sink都上报了barrier就说明这次checkpoint已经走完了。
精确一次性：状态只持久化一次到最终的存储介质中（本地数据库/HDFS)，在Flink下就叫做exactly once（计算的数据可能会重复（无法避免），但状态在存储介质上只会存储一次）。

