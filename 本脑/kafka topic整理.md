
hes-sae-group-\d，dv发送，sae/artifact消费，实时日志topic
alarm, 告警topic，sae/angler生成，ice/artifact消费，实时告警topic
historyAlarm, 历史任务告警topic，sae/angler生成，ice消费，历史任务告警topic
ioc-alarm: 情报回扫告警，shuri发送，ice消费，情报回扫告警topic
qihoosoc-sae-inner: 内部事件topic
monitor: 模块状态监控类topic，metricbeat发送，ha-agent/monitor消费，模块运维监控及HA状态监控用

incident-soar
notification