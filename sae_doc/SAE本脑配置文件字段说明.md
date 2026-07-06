# SAE本脑配置文件字段说明

标签（空格分隔）： SAE_DOC

---

### SAE配置说明

| 配置        | 默认值   |  说明  |
| --------   | -----  | ----  |
| engine.hyperscan.enabled     | false |   是否启用hyperscan做字符串类安全信息的正则匹配    |
| engine.ext-timed-window-optimize        |   true   |   是否启用esper时间窗口优化，该功能实现了当满足条件告警触发后清空时间窗口的数据   |
| engine.num-distinct-event-retained        |    -1    |  是否使用esper内存优化：该功能针对having(distinct())模板，每个distinct+group by分区只保留固定长度的数据，其余清空。-1表示不启用，其他值表示保留数据个数  |
| engine.multi-thread.mode        |    none    |  是否使用esper多线程处理数据，默认none表示不启用，为disruptor表示启用esper多线程模式，创建多个esper，加载不同规则，处理数据  |
| engine.multi-thread.disruptor.thread-num        |    8    |  启用多线程模式时esper创建数量  |
| engine.max_enrich_size        |    500    |  告警触发后各个聚合数组中最多保留的字段值的数量  |
| engine.self_check        |    true    |  是否启用engine health自检  |
| engine.sc_critical_percent        |    98    |  engine health自检内存使用阈值  |
| engine.sc_full_gc_freq_limit        |    2    |  engine health自检1min fullGC次数阈值  |
| server.port        |    8765    |  sae-core开放端口  |
| server.metric_enabled        |    true    |  是否启用metrics report  |
| server.metric_period        |    10    |  metrics频率  |
| distribution.schedule-rotate-delay-millis        |    1000    |  sae规则使能聚合时一级引擎缓存存储数据时间窗口长度  |
| alarm-manager.parallelism        |    8    |  多线程处理告警的线程数量  |
| direction_key        |    默认配置    |  配置direction_key生成所选字段  |

### topic

- alarm-topic: alarm
- inner-topic: qihoosoc_sae_inner
- history-alarm-topic: historyAlarm
- agg-event-topic: qihoosoc-preAgg-event

### direction_key

```
direction_key:
  unknown: ["",""]
  outIn: ["","dst_address"]
  inIn: ["src_address",""]
  inOut: ["src_address", ""]
```

### xdr_config

```
  direction_key:
    edr:
      - client_host_sign
      - _local_date
    ndr:
      - sae_rule_id
      - direction_key
    xdr:
      - sae_rule_id
      - direction_key
  merge_key:
    edr:
      - id
    ndr:
      - src_address
      - dst_address
      - alarm_content
    xdr:
      - src_address
      - dst_address
      - alarm_content
```




