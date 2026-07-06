# SAE分布式测试问题记录及todo list

标签（空格分隔）： SAE_ISSUE

---

### 国保客户现场问题暴露出的可优化点：

 - debug页面增加state size的metric指标展示（降序）
 - debug页面支持设置group by win 降级，只保留n个group
 - fields截取先不做，低优先级的feature
 - follow by的known issue
  - 尽量优化，
  - 指标必须暴露出来


### 测试提出的优化点(todo)：
- 批量启停规则，页面相应慢：目前是一条一条的更新，然后发消息给sae-core，后面看下能否优化，超过一定量，直接reload

## todo list

 - 外部规则加载
 - 自定义function处理逻辑优化
 - 多级节点全局关联分析


 
### 测试覆盖点

 - 功能测试
    1. sae-monitor
     - 规则类型增删改查
     - 规则增删改查
     - 规则导入，内容包导入/页面导入，重复导入，规则运行是否正常，是否正常输出告警
     - 规则导出
    2. sae-core
       测试时注意，需要在不同的运行模式、不同的引擎角色下对各个功能做详细测试。
     - 功能角度
       操作符：当前支持的各种操作符
       过滤条件：过滤条件字段是否存在，是否满足条件，尤其针对自定义函数
       事件源：内部事件/原始事件
       多维度：威胁情报维度/资产维度/脆弱性维度
       数据源：实时数据/历史数据
       模板类型：当前支持的十种模板。上面几个功能测试可只用一种模板类型做详细测试，但各种模板类型也需要做完整测试，验证其有效性。
     - 运行模式角度
       运行模式：单机/集群
       引擎角色：单节点/一级引擎/二级引擎
       集群模式聚合使能与否情况下各个engine的运行是否正常，聚合事件/告警/内部事件是否能正常输出
 
 - 性能测试
  - kafka数据消费：单线程/多线程
  - esper处理：单线程/多线程

 - 调试配置测试
  - 开发自测







### debug相关
 - http://gitlab.hansight.net/root/enterprise-document/wikis/design/debug-api
 - 部分debug接口调整

### 相关问题
 - 前置正序器：集群level-2模式需打开前置正序器，当前前置正序器默认对最近接收到的3s内的数据进行排序输出，不能保证事件的完全正序。另外，单机模式是否需要开启前置正序器？
 - topic配置：之前的hes-sae-group相关topic可移除，直接采用event。集群模式下内部事件仍需要发往dv，交由dv转发
 - 全局白名单：是否需要交给dv来做？
 - sae-monitor是否需要知道当前的运行模式及sae-core相关信息？这主要涉及debug接口改造
   目前想法：redis中存放sae-core相关信息(运行模式，ip:port，消费的kafka server及topic)


spin_tag是为了防止告警多次重报而引入的。
dv原始事件：spin_tag = 0L
内部事件：spin_tag = 1L
威胁情报IP匹配事件：spin_tag = 2L(源地址匹配)；spin_tag = 3L(目的地址匹配)
威胁情报Domain匹配事件：spin_tag = 4L
漏洞利用匹配事件：spin_tag = 10L

规则生成逻辑：
当事件源指定具体事件名称时，无需依据spin_tag做过滤；
当事件源配置为全局事件时，会对过滤条件中有没有spin_tag做check。
过滤条件中，match操作符用于匹配情报，无右操作数，仅针对源地址/目的地址/域名三个字段有效，spin_tag = 2L(源地址匹配)；spin_tag = 3L(目的地址匹配)；spin_tag = 4L(域名匹配)。
如果使用match操作符，会依据条件配置，转换成具体的spin_tag表达式。如果没有spin_tag，会在原来过滤条件基础上加一个与操作，AND spin_tag = 0L。

事件处理逻辑：
内部事件在生成时，会带spin_tag字段，值为1L；
对于shuri发过来的脆弱性数据，sae给数据添加spin_tag字段，值为10L；
对于shuri发过来的威胁情报数据，sae根据ioc_matcher字段给数据添加spin_tag字段，值依据ioc_matcher而定；
对于dv发过来的原始数据，sae给数据添加spin_tag字段，值为0L。


Dears,
  近期看了下我们内置的几个威胁情报类的关联分析规则，发现配置存在一些问题，会导致无法正常触发告警。现说明如下。
  1. 威胁情报事件生成原理：
  威胁情报相关的事件是由shuri模块丰富化后再发到kafka的，shuri会将威胁情报信息丰富化到事件中，修改事件名称为“威胁情报IP匹配事件”或“威胁情报Domain匹配事件”，将原来的事件名称放入“原事件名称”字段中。
  2. 关联分析规则配置要求：
  为了防止告警重报，sae对威胁情报相关规则配置有一定要求：
  - match操作符用于匹配情报，无右操作数，当前仅针对源地址/目的地址/域名三个字段有效；
  - 如果能够确定事件名称，需将事件源名称配置为“威胁情报IP匹配事件”或“威胁情报Domain匹配事件”。
  - 如果不确定事件名称，可将事件源配置为全局事件，但需要在过滤条件中使用match操作符过滤具体的匹配字段。
  3. 当前几个内置规则存在的问题：
  - 3389端口连接后疑似横向移动成功
  域名 match时才生成“威胁情报Domain匹配事件”，该逻辑不成立。
  - 内网主机感染恶意程序-连接恶意IP或域名后下载可疑程序
  事件源为全局事件，需要在过滤条件中指明匹配威胁情报的字段。
  - 内网主机遭受漏洞攻击入侵后主动请求解析恶意域名
  事件名称已修改，需将过滤条件中的事件名称改为原事件名称。

关联分析规则存在一些需要进一步优化的地方，之前整理过一个wiki：http://gitlab.hansight.net/root/enterprise-document/wikis/design/sae-rule-configuration-optimization，以供参考。

多维度关联分析，由shuri实时丰富化
存在问题：
1. 相关规则无法通过执行历史任务验证

脆弱性/威胁情报数据由shuri实时丰富化，原始数据由dv发送，shuri丰富化后会再次发送一次，可能导致重复告警。
当前的解决方法：通过spin_tag区分。我们在生成规则时，如果配置事件源为全局事件，则spin_tag=0，其他的spin_tag设置为依据规则配置而定。这样要求我们在配置规则时，必须指定事件源为具体事件，无法在过滤条件中对事件名称做过滤。内部事件也存在类似问题。

但这样要求我们在配置规则时，必须指定事件源为具体事件。我们在生成规则时，如果配置事件源为全局事件，则spin_tag=0，这样会导致规则不匹配，无法正常生成告警。无法在过滤条件中对事件名称做过滤。
内部事件也存在类似问题。

### kafka消息通知sae功能测试点

#### sae-moniotr
- 消息发送
  - 关联分析规则更新
  - 搜索告警规则更新
  - 规则类型更新
  - 规则导入
  - 规则类型导入
  - 历史任务更新
- 消息接收
  - 事件更新
  - data_source更新
  - 属性更新

#### sae-core
- 消息接收
  - data_source更新
  - 属性更新
  - 情报更新
  - 全局白名单更新
  - 关联分析规则更新
  - 资产更新

#### angler
- 消息接收
  - data_source更新
  - 内网IP情报更新
  - 全局白名单更新
  - 搜索告警规则更新



### esper pattern

#### pattern operator
- 重复性操作符：every, every-distinct, [num] and until
- 逻辑操作符：与或非
- 顺序控制操作符：-> (followed-by)
- 生命周期控制操作符：where-conditions that control the lifecycle of subexpressions. Examples are timer:within, timer:withinmax and while-expression. Custom plug-in guards may also be used.
pattern优化:
- 是否有必要Use the @SuppressOverlappingMatches pattern-level annotation to instruct the engine to discard all but the first match among multiple overlapping matches.
every a=A -> B，A1   A2   B1 ,  {A1, B1}  {A2, B1} 
@SuppressOverlappingMatches [every a=A -> b=B],  {A1, B1}
@SuppressOverlappingMatches
@DiscardPartialsOnMatch 
repeat-until: every [2] (a=A and not C)