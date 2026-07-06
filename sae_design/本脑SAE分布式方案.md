# 本脑SAE分布式方案

标签（空格分隔）： SAE_DESIGN

---

# 百万级EPS分析引擎分布式设计架构

### 目标

 - 能处理百万eps的关联分析，不求解决计算不可并行化的场景
 - 控制住实现的工程难度
 - 强化稳定性与人工干预的能力

### 整体设计思路

将SAE分成两部分：

- sae-monitor：负责与前端页面交互，主要包括规则类型、规则、历史任务。生成规则，交给sae-core engine处理。
- sae-core集群：加载规则，生成告警；执行历史任务。

SAE-CORE集群的节点类型分为两类：

- 全局状态不敏感节点，一级规则引擎，多个，无状态，职能为：
  1. 接收DV日志
  2. 加载触发类规则，进行匹配，生成告警
  3. 对接收事件进行过滤和定时统计，定时输出预聚合事件（在指定窗口期对某种类型事件的某些字段的聚合统计），实现数据降级
  4. 加载不使能聚合的规则的过滤条件拼接构成的大规则，输出匹配的原始事件
- 全局状态敏感节点，二级规则引擎，单个，有状态，职能为:
  1. 接收一级规则引擎生成的预聚合事件
  2. 加载统计类及关联分析类规则，对接收数据进行关联分析，生成告警。

### 架构示意图
![分布式架构][./misc_photo/分布式架构.png]

### 分布式方案具体说明：

- 数据分流：  
  DV负责依据数据分流，把分流数据交给多个一级engine。在现场具体部署时，先要根据数据量确定一级engine的数量。dv将数据发往不同的topic，每个一级engine加载一个topic来消费。  

- 预聚合事件：  
  预聚合事件是指在指定窗口期根据一些设定条件对事件的某些字段做聚合统计后输出的事件。由一级规则引擎生成后交给二级规则引擎处理。可以通过页面配置选择是否通过聚合生成预聚合事件。  
  预聚合事件中需携带触发其生成的所有原始日志的id合集，以便告警溯源。  
  预聚合事件中需携带规则id信息，以便二级规则知晓规则id正确匹配并生成告警。目前的做法是预聚合事件的事件名称携带规则id信息，二级规则只需匹配相关预聚合事件的名称即可。

- 规则生成逻辑：  
  * 需配置聚合使能的规则模板类型：     
  统计类规则模板，包括having count,having count distinct, having sum.  
  关联分析类规则模板，包括follow-by, or-follow-by, not-follow-by, not before, no order.  
  针对这一类规则，根据规则的使能配置生成不同的一级规则和二级规则，供一级engine和二级engine加载。  
  * 无需配置聚合使能的规则模板类型：    
   普通模板，该模板规则属触发类规则，一个事件即可触发告警，无需配置使能聚合，生成预聚合事件。  
   repeat-until模板，如果生成预聚合事件，A事件通过规则无法表达，暂不支持配置使能聚合，生成预聚合事件。  
  * 对于使能聚合配置的规则：    
  一级规则为普通模板规则语句，通过加载过滤条件来过滤事件，对事件字段做聚合统计，聚合主要涉及count/sum/distinct/window。定时生成预聚合事件，暂定每1s输出一次，预聚合事件发生时间取当前时间窗口内的所有事件发生时间的最小值。    
  二级规则模板格式不变，过滤条件有变，根据预聚合事件名称做过滤，匹配预聚合事件，生成告警。  
  * 对于没有使能聚合配置的规则：    
  一级规则为一个大规则，过滤条件由所有这些规则进行或逻辑生成。此外，repeat-until模板类规则的过滤条件也放入该规则中，以达到满足触发条件交给二级engine处理的目的。   
  二级规则为既有规则。    

- 不同类型规则引擎规则加载逻辑：  
  * 一级engine加载全量规则，它加载的规则有三类：  
   触发类规则，直接生成告警  
  使能聚合类规则，定时输出预聚合事件给二级engine  
  明确定义不统计的所有规则的过滤条件or逻辑生成的大规则，输出原始事件给二级engine  
  * 二级engine加载的规则有两类：  
  统计指标类规则的二级规则  
  明确定义不做聚合统计的所有规则  

### 其他  

- 二级engine加载前置正序器
- 历史任务交由二级engine处理  
- 如果一级engine数据降级并不成功，需人工接入，根据事件名称对事件进行分流。

### Known Issues  

 - TI/Vulnerability信息交由shuri丰富化，shuri吞吐量能否满足需求。  
 - 多维度关联分析的丰富化数据是实时补充的，相关规则历史任务无法验证。讨论认为，读取es的操作可交给dv来做，shuri丰富化后再给engine处理，这样即可避免这个问题。  
 - 容易导致重复告警。目前的做法是添加spin_tag标记字段， 对dv/shuri发来的数据做不同的标记，并在规则中添加标记字段过滤条件，以避免重复告警。如果配置威胁情报匹配事件相关规则，需指定事件源为该事件，这样导致一个问题，如果想匹配威胁情报ip或domain匹配事件需配置两个规则。目前继续这样。  
 - 资产维度数据为sae自己获取，与另外两个维度不统一。一级engine和二级engine都需要加载资产数据。目前继续这样。  


### 附录  

使能聚合配置的规则具体生成逻辑见下：    

| templateType| level-1-engine | level-2-engine | remarks |
|---|---|---|---|
| normal                | epl: select select_fields... from GlobalEvent(fiter_condition)<br/>output: alarm | null                                                         | level-1-engine addListener，生成告警。                       |
| having count          | epl: select * from GlobalEvent(fiter_condition)<br/>自定义EPStatement获取最后一笔事件、聚合字段、事件数量<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields, count_data) | epl: select select_fields, windowAgg_fileds... from GlobalEvent(trigger_event).win:ext_timed(xxx) group by group_by fields having sum(count_data) condition<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值及计数，level-2-engine addListener生成告警。 |
| having sum            | epl: select * from GlobalEvent(fiter_condition)<br/>自定义EPStatement获取最后一笔事件、聚合字段、字段和<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields, sum_data) | epl: select select_fields, windowAgg_fileds... from GlobalEvent(trigger_event).win:ext_timed(xxx) group by group_by fields having sum(sum_data) condition<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值及求和，level-2-engine addListener生成告警。 |
| having count distinct | epl: select * from GlobalEvent(fiter_condition)<br/>自定义EPStatement获取最后一笔事件、聚合字段、distinct字段归入group by字段输出<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields | epl: select select_fields, windowAgg_fileds... from GlobalEvent(trigger_event).win:ext_timed(xxx) group by group_by fields having count(distinct(distinct_field)) condition<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，预聚合事件按照groupby字段及distinct字段分组，需包含输出字段/聚合字段/分组字段值及distinct字段值，level-2-engine addListener生成告警。 |
| follow by             | A: <br/>epl: select * from GlobalEvent(fiter_condition_A)<br/>提取关联条件中A相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>B: <br/>epl: select * from GlobalEvent(fiter_condition_B)<br/>提取关联条件中B相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields) | epl: select select_fields... from pattern[every A=Globalevent(trigger_event_A)->(B=Globalevent(trigger_event_B and related_condition) where timer:within(xxx)) while time_condition]<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值，level-2-engine addListener生成告警。 |
| or follow by          | A: <br/>epl: select * from GlobalEvent(fiter_condition_A)<br/>提取关联条件中A相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>B: <br/>epl: select * from GlobalEvent(fiter_condition_B)<br/>提取关联条件中B相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields) | select select_fields... from pattern[(every A=GlobalEvent(trigger_event_A)->(trigger_event_B and related_condition) where timer:within(xxx) while time_condition) or (every B=GlobalEvent(trigger_event_B)->(A=GlobalEvent(trigger_event_A and related_condition) where timer:within(xxx)) while time_condition)]<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值，level-2-engine addListener生成告警。 |
| not follow by         | A: <br/>epl: select * from GlobalEvent(fiter_condition_A)<br/>提取关联条件中A相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>B: <br/>epl: select * from GlobalEvent(fiter_condition_B)<br/>提取关联条件中B相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields) | select select_fields... from pattern[every A=GlobalEvent(trigger_event_A) -> (timer:interval(xxx) and not B=GlobalEvent(trigger_event_B))]<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值，level-2-engine addListener生成告警。 |
| not before            | A: <br/>epl: select * from GlobalEvent(fiter_condition_A)<br/>提取关联条件中A相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>B: <br/>epl: select * from GlobalEvent(fiter_condition_B)<br/>提取关联条件中B相关的属性作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段、事件数量<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields) | select select_fields... from pattern[every (A=GlobalEvent(activeTimeCheck and updateNbfState((trigger_event_A), other_params)) or B=GlobalEvent(isNotBefore((trigger_event_B), other_params)))]<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值，level-2-engine addListener生成告警。 |
| no order             | A: <br/>epl: select * from GlobalEvent(fiter_condition_A)<br/>提取分组条件中的属性字段作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>B: <br/>epl: select * from GlobalEvent(fiter_condition_B)<br/>提取分组条件中的属性字段作为groupBy字段，自定义EPStatement获取最后一笔事件、聚合字段<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields)<br/>C: <br/>... | epl: select irstream * FROM GlobalEvent(((trigger_event_A) AND onCase(rule_id, event_order, event_count, event, group_by_fields)) OR ((trigger_event_B) AND onCase(rule_id, event_order, event_count, event, group_by_fields)) OR ((trigger_event_C) AND onCase(rule_id, event_order, event_count, event, group_by_fields))).win:ext_timed(occur_time, 10 min) HAVING (TRUE)<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值，level-2-engine addListener生成告警。 |
| repeat until          | null | select select_fields... from pattern[every [limit] A=GlobalEvent(fiter_condition_A)->(B=GlobalEvent(fiter_condition_B and related_condition) where timer:within(xxx)) while time_condition]<br/>output: alarm | level-2-engine addListener，生成告警。该模板无法表达A事件repeat limit，对agg不做支持。可通过大规则对事件进行过滤后交给二级engine来处理。 |
| not occur          | epl: select null from GlobalEvent(fiter_condition)<br/>自定义EPStatement获取最后一笔事件、聚合字段、事件数量<br/>output: performance_event(trigger_event, id, occur_time, select_fields, windowAgg_fileds, groupBy_fields, count_data) | epl: select null from GlobalEvent(isNotOccur(rule_id, A, 'occur_time', 5000, (trigger_event)))<br/>output: alarm | level-1-engine setSubscriber生成预聚合事件，需包含输出字段/聚合字段/分组字段值及计数，level-2-engine addListener生成告警。 |

### 多级节点之间关联分析

- 多级节点之间的内网配置还有安全信息需保持一致
- 在SAE规则里添加“多级关联分析”的配置选项
  1. 在各个子节点人工配置需要做多级关联分析的规则（依赖一线操作人员或者客户）
  2. ~~在父节点配置之后由父节点统一下发到子节点（父节点需要添加子节点的配置、规则更新之后需要通知来同步）~~
- 子节点中对配置了“多级关联分析”的规则做转换，抽取出其中的事件名称加过滤条件，配置了几个事件就抽取几条规则
- 子节点匹配到对应的事件发送到父节点
  1. 发送到本节点kafka的特定topic，由父节点dv配置单独的数据源进行处理（dv需要添加对应的解析规则还是需要特殊处理？）
  2. ~~直接发送到父节点kafka的“hes-sae-group-0” topic（子节点需要配置父节点的kafka地址，数据无法均衡）~~
- 父节点接收对应数据之后不写es，只做关联分析，告警溯源由es多集群来保证


  [1]: http://static.zybuluo.com/misasagi/vwuh4293uwl3azhcspvm20ga/%E5%88%86%E5%B8%83%E5%BC%8F%E6%9E%B6%E6%9E%84.png