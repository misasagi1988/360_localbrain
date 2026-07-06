# Qradar

标签（空格分隔）： MARKET_RESEARCH

---

## Qradar link

Qradar SIEM link: https://myibm.ibm.com/dashboard/, 14天有效期
用户名/密码: 846061273@qq.com/Misasagi1988
user guide: https://www.ibm.com/support/knowledgecenter/SS42VS_7.3.2/com.ibm.qradar.doc/b_qradar_users_guide.pdf
admin guide: https://www.ibm.com/support/knowledgecenter/SS42VS_7.3.3/com.ibm.qradar.doc/b_qradar_admin_guide.pdf

## Qradar architecture(3 layers)

### Data Collection(Event collector, Flow collector, parse&normalize data)

- QRadar Event Collector
  The Event Collector collects events from local and remote log sources, and normalizes raw log source events to format them for use by QRadar. The Event Collector appliances do not store events locally. Instead, the appliances collect and parse events before they send events to an Event Processor appliance for storage.
- QRadar QFlow Collector
  The Flow Collector collects flows by connecting to a SPAN port, or a network TAP. 

### Data processing(data storage, run in custom rule engine, generate alert&offenses)

- QRadar Event Processor
  The Event Processor processes events that are collected from one or more Event Collector components. The Event Processor processes events by using the Custom Rules Engine (CRE). If events are matched to the CRE custom rules that are predefined on the Console, the Event Processor executes the action that is defined for the rule response.
Each Event Processor has local storage, and event data is stored on the processor, or it can be stored on a Data Node.
The processing rate for events is determined by your events per second (EPS) license. If you exceed the EPS rate, events are buffered and remain in the Event Collector source queues until the rate drops. However, if you continue to exceed the EPS license rate, and the queue fills up, your system drops events, and QRadar issues a warning about exceeding your licensed EPS rate.
- QRadar Flow Processor

### Data searches(Graph&report, alert&offenses, user interface)

The QRadar Console provides the QRadar user interface, and real-time event and flow views, reports, offenses, asset information, and administrative functions.

## Qradar中的一些概念

- Building Block 类似安全信息组
- Building blocks are tested before rules are tested.
- Rule 分类:
 - Custom rules perform tests on events, flows, and offenses to detect unusual activity in your network.
 - Anomaly detection rules perform tests on the results of saved flow or event searches to detect when unusual traffic patterns occur in your network.
- reference set
reference set可以用于规则过滤条件，也可配置在告警输出响应操作中。
包含set name, 元素类型，元素过期时间，元素过期策略
对于其中的每一个元素：元素值、剩余时间，上次碰撞时间
可以根据reference set获取引用该set的相关规则的具体信息
数据元素过期时，会触发生成reference data过期事件，包含reference set名称及过期元素值


## not occur
Learn more about using rules for events that are not detected:
The following rule tests can be triggered individually, but rule tests in the same rule test stack are not
acted upon.
• when the event(s) have not been detected by one or more of these log source types for this
many seconds
• when the event(s) have not been detected by one or more of these log sources for this many
seconds
• when the event(s) have not been detected by one or more of these log source groups for this
many seconds
These rule tests are not activated by an incoming event, but instead are activated when a specific
event is not seen for a specific time interval that you configured. QRadar uses a watcher task that
periodically queries the last time that an event was seen (last seen time), and stores this time for the
event, for each log source. The rule is triggered when the difference between this last seen time and
the current time exceeds the number of seconds that is configured in the rule.

