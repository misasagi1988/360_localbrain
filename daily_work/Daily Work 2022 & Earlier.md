# Daily Work 2022 & Earlier

标签（空格分隔）： 360BrainSecurity

---

### 2020-07-13

 - sae分布式规则转换部分代码优化，build及test
 - 多级节点之间关联分析功能方案讨论
 - 客户现场问题排除记录、多级节点关联分析功能的文档整理

### 2020-07-14

 - sae分布式代码合入360-brain-dev
 - 生成build

### 2020-07-15

 - sae分布式单机模式各个模板规则测试及bugfix
 - 熟悉消息通知由redis改为kafka通用模块使用方法

### 2020-07-16

 - 建行告警id生成问题support
 - sae-monitor模块，通知消息发送方式由redis改为通过kafka后影响代码改动
 - sae-monitor模块，通知消息接收方式由redis改为kafka后的影响代码改动
 - sae分布式todo list整理及任务安排

### 2020-07-17

 - sae-core模块，通知消息接收方式由redis改为kafka后的影响代码改动
 - 王震客户现场，单机模式新部署，sae不生成告警原因分析：从现场log来看，sae没有任何问题，可以正常生成告警相关数据，但由于规则限制，生成的数据均为内部事件告警，从sae的debug页面可以正常拿到告警数据。鉴于页面无法访问，推荐其使用外部规则验证sae准确性。

### 2020-07-20

 - angler模块，通知消息接收方式由redis改为kafka后的影响代码改动
 - 数据分析模块中关于瀚思(hansight)字样的文字调整

### 2020-07-21

 - 东风日产和农业银行两个6.0GM项目都出现系统监控智能分析工作节点不展示实时处理eps问题分析，最终定位到是kafka多线程处理时没有对日志数据做metrics统计，已fix并提供patch
 - sae分布式历史任务部分测试，not-before模板历史任务执行有问题，自定义函数考虑的都是实时场景，没有针对历史任务的处理逻辑，在修复中。repeat-until及no-order模板尚未测试。

### 2020-07-22

 - sae分布式历史任务部分，not-before模板、repeat-until及no-order模板测试及发现的问题bugfix(not-before模板，实时与历史任务listener单独创建)。
 - 历史任务bugfix，初始化时需加载db中pending的job，执行。***当前历史任务实际上还是存在问题的，尚未完成的历史任务，stop后如果sae重启，runningTime不会从startTime开始，会导致部分状态丢失，告警漏报。***
 - 农行司扬，关联分析规则无法正常生成告警问题support，分析发现是他们自己构造的数据本身有问题。

### 2020-07-23

 - sae分布式debug接口调整
 - 农行follow-by模板规则(A为内部事件，B为正常事件)告警无法生成问题分析及bugfix，分析发现规则会对事件id做check，A.id!=B.id，但内部事件没有id字段，导致告警无法正常生成。解决办法：给内部事件赋id字段，值取event_id字段的任意一个。保证溯源id都是有效的。
 - 建行历史任务问题答疑及support

### 2020-07-24

 - sae分布式实现原理介绍
 - sae分布式debug接口调整
 - 通知消息发送方式由redis改为通过kafka，sae代码改动

### 2020-07-27

 - 农行not-follow-by规则无效原因分析及bugfix
 - sae分布式build
 - sae bugfix【ID1004731】SAE非内置规则从环境A导入到环境B或者重复导入内容包，对应的规则ID在数据库里可能会不一致，主要原因：NBF/No-Order规则模板epl中携带规则id信息，但生成的规则epl中没有沿用老的规则id，而是新生成规则id，导致epl的id与规则id不对应。
- sae bugfix 【ID1004722】not_before模板的SAE规则不生效，没有生成告警

### 2020-07-28

 - 安全同事答疑
 - sae分布式build test support
 - esper自定义function优化

### 2020-07-29

 - 安全同事答疑，告警误报，从现场数据来看，告警是7.20生成的，读取db记录，7.20有对相关规则做过更新，无法确定更新前规则的配置；而且执行历史任务，也没有误报。只能怀疑是老规则配置不合理导致生成了有问题的告警，所以做了修改，后面再观察吧，看下问题还能复现。
 - sae分布式测试覆盖点整理
 - sae分布式测试support&bugfix

### 2020-07-30

 - sae分布式测试support&bugfix
 - 6.0GM版本，sae patch改动记录
 - 资产/脆弱性字段改动，sae配合修改(涉及字段os -> operating_system)

### 2020-07-31

 - sae分布式测试support&bugfix
 - 资产/脆弱性字段改动，属性字段配合修改

### 2020-08-03

 - sae分布式测试support&bugfix
 - sae halite bugfix，metaData并非只有alarm，alarm/event都需要读取

### 2020-08-04

 - sae分布式测试support&bugfix
 - 360 demo环境having count distinct模板告警误报问题分析

### 2020-08-05

 - sae分布式测试support&bugfix
 - 360 demo环境模板告警误报问题复现/分析/bugfix
规则配置：having count(distinct(dst_address)) >= 20触发告警，但生成的告警中，目的地址组元素数量不到20。 
问题说明：调试发现，是之前修改esper源码导致的问题：
针对统计类规则，为了触发告警后将状态清零，我们对源码进行了修改，增加了clearTag变量，记录上次移除前的状态，以便下次remove的时候先移除上次的状态。但clear/leave function处理存在问题。
前段时间倚天改了一下esper源码，触发后就把timewindow的数据清掉了，这个clearTag也就没有用了，所以我们又将Esper中clearTag的机制移除，恢复为之前的源码。
统计类规则的3个模板应该都存在这个问题。目前已经修复。
 - 建行客户关联分析任务卡顿问题support，目前我们的历史任务执行是依次顺序执行的，不支持并发，建行客户频繁创建，任务执行速度不满足其要求。目前的方案是提高一次读取es的日志量，并建议其单个任务中加载多个规则。

### 2020-08-06

 - 建行定制分支历史任务es_scroll_size可配置，默认10000
 - 建行历史任务执行卡顿问题support，提出建议(单条历史任务跑多个规则;使用hqlite做过滤)
 - sae分布式测试support&bugfix
 - sae规则导入涉及的各种计数存在错误bugfix

### 2020-08-10

 - 建行6.0beta版本sae-core distinct告警误报问题support(distinct字段数量不满足条件即告警，6.0beta尚未合入esper优化代码，跟之前不是同一个问题)，尚未复现，没有定位到问题具体原因
 - sae分布式测试support&bugfix

### 2020-08-11

 - sae分布式测试support&bugfix
 - 建行distinct模板告警误报问题support，新换了一个build之后暂时没有出现问题

### 2020-08-12

 - sae分布式测试support&bugfix

### 2020-08-13

 - sae分布式distinct模板规则优化思考
 - 搜索告警规则导入使能bugfix
 - 当前内容包威胁情报规则存在问题整理

### 2020-08-14

 - sae本脑630 bugfix patch
 - sae分布式 test support
 - redis改为kafka消息处理功能合入360本脑分支

### 2020-08-17

 - sae分布式 test support
 - 国家保密局SAE分布式护网客户现场问题support，多个sae-core消费group重复，通过log来看是zk问题，sae-core频繁检测到节点被remove，不停的抢占及消费topic。

### 2020-08-18

 - sae hotfix-rel630
 - 东航客户3.7环境cep威胁情报类规则无法生成告警问题support
 - 本脑威胁情报相关改动问题整理

### 2020-08-19

 - 本脑威胁情报相关改动，sae实现方案思考，esper文档review
 - sae hotfix-rel630 not-before模板未生成告警原因分析
 - 预聚合事件输出优化，_array分两种输出(list/set)，debug输出优化，去除_array字段
 - 现场rel630历史任务执行无告警生成问题定位，to be continued

### 2020-08-20

 - 国家应急部现场rel630普通模板规则历史任务执行无告警生成问题定位，最终定位到数据有写入es，但后端查询接口错误，没有返回数据
 - 国家应急部现场rel630普通模板规则无法正常生成实时告警问题定位，最终定位到是dv问题，数据没有发到kafka，解析规则也有问题
 - 南京国税短信通知问题check
 - 预聚合事件生成优化

### 2020-08-21

 - 宁波卫健委530alpha版本样本鉴定事件普通模板事件告警无法正常生成问题定位：解析规则有问题，file_name/file_md5字段为数组类型，数据中数组元素都是null，导致sae抛空指针异常，数据未进入esper分析。
 - 建行历史任务无法执行问题定位
 - 建行普通模板规则停用删除无效，告警仍不断生成问题定位：调用reloadRule接口，停掉相关数据的数据源后告警数据最新时间不再更新，虽数据量不断上涨，估计是ice问题，告警数据量大，一时处理不过来导致。大概半小时后，告警总量不再更新。重新开启数据源，不再有相关告警生成。
 - 建行or-follow-by规则告警重复原因定位：猜测是集群模式导致的问题：规则中两个事件源都配置的全局事件，分布式情况下会生成两个临时事件，溯源的两个事件都满足AB的过滤条件，导致两个事件过来会生成四个临时事件，导致重复告警。
 - sae分布式 test support

### 2020-08-24

 - 建行or-follow-by规则告警重复原因定位：两个事件过滤条件完全一样，使用or-follow-by会有这个问题，模板选择错误，建议选择distinct/follow-by模板。
 - sae分布式 test support & bugfix


### 2020-08-25

 - sae分布式 test support & bugfix， 预聚合事件输出时间窗口配置字段

### 2020-08-26

 - 搜索告警模块bugfix及代码优化，默认direction_key修改
 - 内测环境sae-core不生成告警问题分析
 - sae-core故障排查手册整理

### 2020-08-27

 - 搜索告警模块bugfix，告警溯源条件优化，去除无关日志
 - sae-core故障排查手册进一步整理
 - 系统监控规则讨论

### 2020-08-28

 - 保密局客户现场问题support
 - 威胁情报类规则重构改动设计方案思考
 
### 2020-08-31

 - 威胁情报类规则重构
 - 保密局客户现场sae分布式zk断线问题support

### 2020-09-01

 - 威胁情报类规则重构
 - 保密局客户现场sae分布式support
 - 马上金融客户现场sae问题support
 - 中央国债客户现场，某一时间段无新告警生成问题support

### 2020-09-02

 - 威胁情报类规则重构
 - 保密局客户现场sae分布式support，dump文件分析，问题定位(规则影响，内存占用率过高)
 - 客户问题反映的问题及后续优化思路讨论(group-by分组太多，follow-by A事件太多)

### 2020-09-03

 - 威胁情报类规则重构问题讨论
 - 全局关联分析问题讨论

### 2020-09-04

 - 分规则的分布式方案实现讨论
 - 中央国债SAE不告警问题分析support，定位是group-by规则内存占用率过高导致
 - 基于SIM模型的多维度关联分析规则重构

### 2020-09-07

 - 基于SIM模型的多维度关联分析规则重构

### 2020-09-08

 - SAE全局关联分析功能开发

### 2020-09-09

 - 中央国债客户--某一时段SAE无新告警生成问题support

### 2020-09-10

 - TAPD bugfix(sql查询特殊字符转义，alg logback)

### 2020-09-11

 - TAPD bugfix(历史任务)
 - 客户问题support(威胁情报普通模板规则，生成内部事件，导致威胁情报事件重复发给sae，告警量剧增)
 - (360威胁情报重构/sae规则配置优化)test case review

### 2020-09-14

 - 客户问题support(中国人寿distinct规则不能正常触发告警；
中交建6.0GM一个事件就触发告警"账号登录异常-短时间内在不同IP登录成功"；告警时间与日志时间不对应)
 - 新分布式方案distinct模板规则优化
 - 多维度关联分析重构合入360-brain-dev

### 2020-09-15

 - 新分布式方案distinct模板规则优化自测
 - 消息通知文档整理，sae规则配置文档整理

### 2020-09-16

 - sae规则配置文档整理
 - sae规则优化：filter语句中额外补充group by字段存在条件
 - sae规则优化：fix bug 【ID1005778】distinct规则，distinct_data字段数据过多，依据条件增加输出限制
 - 算法模块response check，不要输出异常stack trace信息

### 2020-09-17

 - sae规则配置文档整理
 - sae 功能优化，ice edr场景受害者组字段修改
 - sae bugfix

### 2020-09-18&19

 - sae规则配置sharing
 - sae 多维度关联分析 test support

### 2020-09-21

 - sae 多维度关联分析 test support

### 2020-09-22

 - sae 多维度关联分析 test support
 - 百胜告警无法生成原因分析，rlike .不支持\n所致

### 2020-09-23

 - sae 多维度关联分析 test support，规则配置文档wiki整理

### 2020-09-24

 - sae like/rlike操作符规则转换重构

### 2020-09-27~28

 - sae规则检查工具开发，指出当前内容包环境规则中的几个问题：
  - 统计类规则，触发条件>=1
  - 未启用告警及内部事件，导致规则无效
  - 过滤条件、关联条件理解错误，在关联条件中配置某一事件的过滤条件
  - 内部事件与普通事件重名
  - 内部事件名称不合适(建议以“内部事件-”开头)
  - 普通模板生成内部事件
  - 规则引用事件不存在
  - 内部事件没有被任何规则使用
  - 内部事件输出字段不完整，引用内部事件的规则无效
  - 规则过滤条件/关联条件中使用的事件的字段不在事件所属sim模型内，导致页面显示有问题

### 2020-09-29~30

 - 用户自定义attck相关信息输出，解析规则需将数据放入attack_id字段，格式：tacticID + "_" + techniqueID
 - 内容包环境sae规则更新support

### 2020-10-09~10

 - sae全局关联分析方案思路整理
 - sae-monitor全局关联分析功能开发：节点消息变动处理，kakfa io object类
 - 浦发客户5.5环境sae规则告警误报support

### 2020-10-12

 - sae-monitor全局关联分析功能开发：sae-monitor规则适配改动，子节点接收后的规则消息处理

### 2020-10-13

 - sae-monitor全局关联分析功能开发：sae-monitor父节点全局使能规则消息发送，规则导出逻辑变动(只导出本节点规则，全局使能开关disable，nodeChain置null)；节点变动消息处理

### 2020-10-14

 - sae-monitor全局关联分析功能开发功能自测&bugfix

### 2020-10-15

 - sae-monitor全局关联分析获取规则接口修改，适配历史任务

### 2020-10-16

 - sae-core全局关联分析功能开发 

### 2020-10-19

 - 本节点规则node_chain为null修改(方便升级) 
 - 全局关联分析功能自测

### 2020-10-20

 - 百胜sae分布式，多个sae-core重复消费topic问题定位与解决
 - 百胜sae分布式，多个topic eps过大，sae处理能力达到上限，数据无法被消费，告警数据骤减问题，给出数据人工分流的解决方案。
 - IBM Qradar research

### 2020-10-21

 - 内测环境，domain威胁情报类告警漏报问题分析，15、19号，6个满足条件的日志，只有2个生成告警。原因：规则21号有修改，去除了源地址belong内网IP过滤条件。

### 2020-10-22

 - 华为sae问题jar包update&repack。
 - 下午及23号team building

### 2020-10-26~30

 - sae全局关联分析debug 

### 2020-11-02

 - sae全局关联分析build&提测
 - sae全局关联分析的进一步优化思路

### 2020-11-03

 - 分析引擎design&coding分享

### 2020-11-04

 - 全局关联分析bugfix，duplicate模式暂定只有0号sae-core加载规则；进一步优化思路整理
 - 了解本脑sae性能测试结果&报告
 - angler代码回顾

### 2020-11-05

 - shuri代码review&改进建议

### 2020-11-06

 - sae全局关联分析问题定位，目前没有找到问题原因
 - 6.0升本脑sae规则导入问题check。6.0升级本脑后，部分属性type有变化，导致epl语句编译失败，需重启tomcat，规则导入方可正常。建议属性导入后重启tomcat/sae/incident再导入规则。
 - 6.0升本脑sae历史任务规则无法正常显示问题check。历史任务保存的是执行规则id，升本脑采用的做法是规则导出后重新导入，规则id有变化，导致页面无法正常显示。建议升级时清空sae/ice历史任务相关table

### 2020-11-09

 -  6.0升本脑sae规则导入优化：目前修改了下sae规则的导入逻辑，导入时，如果id在db中不存在，则使用原有id，如果已存在，则重新生成id。这只是临时的解决方案，而且要求升级时先导入原有的sae规则。后面需要优化下规则的id生成算法。

### 2020-11-10

 -  开发6.0升本脑sae规则导入工具，讨论后无用废弃，改为不删除原有table，直接在原有table上改造，以保证原有规则仍占有所持id
 -  sae全局关联分析bugfix(nodeChain=""导致是否为父节点规则判断错误；子节点数据只对父节点全局关联分析规则生效，其他规则无用，语句中增加filter条件)

### 2020-11-11~12

 -  全局关联分析bugfix
 -  repeat-until模板规则不生效问题分析

### 2020-11-13

 -  内部事件/全局事件不走dv，sae自己做负载均衡功能开发
 -  关联分析规则添加标签功能开发

### 2020-11-16

 -  内测环境EDR行为分析类告警无法溯源问题分析

### 2020-11-17

 -  关联分析规则页面优化功能自测
 -  全局关联分析bugfix，创建kafkaOut时因为子类父类初始化顺序问题导致singleTopic对象初始化错误，多个线程发送告警时因为emit中多次对atomInteger操作，没有加锁，线程同步问题导致告警发送失败

### 2020-11-18

 -  Qradar支持业务场景分享会
 -  关联分析规则优化新功能实现
 -  全局关联分析bugfix，sql错误导致注销时子节点没有删除父节点相关规则

### 2020-11-19

 -  关联分析规则优化新功能自测
 -  全局关联分析bug分析，bug ID1006490，父节点环境挂掉后，子节点sae kafka没有检测到这种情况，父节点重启后，子节点sae也没有重新与父节点kafka建立连接。自测不会出现这种情况。具体原因未知。
 -  安全同事support

### 2020-11-20

 -  资产&脆弱性维度关联分析功能开发
 -  分析模块配置文件密码加密功能实现

### 2020-11-23

 -  分级部署(所有下级节点信息在数据表中都有保存，需要根据当前节点id得到直属子节点)，全局关联分析逻辑修改
 -  分级部署，子节点重连kafka后，父节点无法正常生成告警原因分析：从log来看，是字段类型不匹配导致的esper在做select聚合处理时抛异常。

### 2020-11-24

 - 威胁情报Url匹配逻辑
 - 规则标签精确匹配bugfix
 - 分级部署bugfix：注销后在注册，没有重新创建kafka producer，导致数据没有发给父节点。

### 2020-11-25

 - sae威胁情报Url匹配适配修改&自测
 - 告警输出ATTCK逻辑修改

### 2020-11-26

 - 告警输出ATTCK逻辑修改&自测
 - sae威胁情报Url匹配功能测试&合入dev
 - 分析模块本脑1.0sp1版本starter-dependencies修改；配置文件加密功能合入dev
 - 内测环境一sae规则无法生成告警原因分析，最终定位到是规则epl语句有问题，belong操作数没有转成对应的信息组id，导致规则无法生效。后面需加一下这部分的逻辑check。

### 2020-11-27

 - sae规则epl生成时针对安全选项组id做校验
 - 程序启动时自行创建globa rule topic，fix bug ID1006397，避免子节点规则消费延迟。

### 2020-11-30

 - 整理sae分布式相关文档，更新wiki
 - 百胜sae告警骤减原因分析，猜测是zk监听器多线程处理节点变动的影响
 - 内测环境境一sae规则无法生成告警原因分析，最终定位到是数据源配置有问题，数据没有发到kafka给sae消费。

### 2020-12-01

 - hotfix-rel5.0基于zookeeper的分布式代码修改，多线程同步(eps更新，zk监听节点变动消息处理)问题导致eps数据有误，节点变动时sae-core因eps统计错误导致无法正常创建topic消费数据问题的定位&修复。
 -  sae&ice适配安全信息类型修改

### 2020-12-02

 - 百胜客户现场sae-core patch使用support


### 2020-12-03

 - 内测环境重复告警原因分析，未定位到具体原因，reload时删除所有规则抛异常，已添加debug端口方便后面复现时调试。猜测是直接对db操作导致。
 - 审计日志重构：sae&alg模块api接口添加相关日志

### 2020-12-04

 - 建行，having count(*)模板支持配置distinct字段
 ```
 template raw entity:
 {"desc":"某个事件数目次数","hasContext":false,"hasFilter":true,"hasGroupBy":true,"hasHaving":true,"hasSelect":true,"hasWindow":true,"having":{"descTpl":"个数 {{n2:select:[>,<,>=,<=,=,!=]}} {{n3:number:10}}","eplTpl":"count(*) {{n2:select:[>,<,>=,<=,=,!=]}} {{n3:number:10}}","descDist":"DISTINCT字段{{d1:select2:fields}}的个数 {{d2:select:[>,<,>=,<=,=,!=]}} {{d3:number:10}}","eplDist":"count(distinct({{d1:select2:fields}})) {{d2:select:[>,<,>=,<=,=,!=]}} {{d3:number:10}}"},"id":5,"name":"普通模板-having count(*)","patternOperator":"followBy","system":0,"systemBuiltin":false,"templateStatisticType":"COUNT","templateType":"STATISTIC","type":"normal"}
 ```
 - 安全信息重构，sae功能测试

### 2020-12-07

 - 建行，having count(*)模板支持配置distinct字段功能自测
 - having count(*)模板支持配置distinct字段合入360-brain-dev分支
 - attck功能合入dev分支
 - 搜索告警支持sim代码修改

### 2020-12-08

 - sae&angler SIM改造
 - Qradar讨论会

### 2020-12-09

 - sae&angler SIM改造
 - 资产&脆弱性test support

### 2020-12-10

 - 资产&脆弱性test support & bugfix

### 2020-12-11

 - 资产&脆弱性test support & bugfix

### 2020-12-14

 - 资产&脆弱性test support & bugfix
 - 告警SIM化support
 - 规则模板命名优化

### 2020-12-15

 - 搜索告警，es聚合回顾

### 2020-12-16

 - 建行需求，理清思路，搜索告警支持某字段值在所有值中的占比满足条件输出告警

### 2020-12-17

 - 开发建行需求，定制angler支持ratio模式

### 2020-12-18

 - 继续开发建行需求，定制angler支持ratio模式，debug

### 2020-12-21

 - angler ratio bugfix:添加聚合排序逻辑，根据不同的操作符定义聚合时的排序方法。

### 2020-12-22

 - angler ratio功能运行环境测试
 - 内容包导入重构、规则id转为字符串修改等合入dev后build问题test support
 - 整理当前sae规则存在的问题

### 2020-12-23

 - 搜索告警/sae历史任务搜索日志时自动过滤event_type为/other/other类型
 - 全局关联分析规则bugfix：子节点不允许删除，导出规则全部为非本节点规则时给出提示。

### 2020-12-24

 - 搜索告警支持reload；submission定时任务部分代码优化(使用官方定时任务工具类，stop/delete时设置标记位，reload时stop所有子任务)

### 2020-12-25

 - 搜索告警支持reload bugfix
 - jvm，类加载子系统学习

### 2020-12-28

 - 测试环境问题support
 - 建行搜索告警起止时间改为本次check的起止时间，与时间窗口相关，而不是取相关日志的时间。

### 2020-12-29

 - 整理tapd上的bug
 - 测试环境问题support，解决代码合并后出现的一些问题
 - sae&ice安全信息改动合入dev
 - 37内容包环境is_directory属性id为空问题support
 - 安全同事195.4环境问题support, id不是告警模型的必选字段，告警页面无法展示 告警id信息，导致无法从告警页面直接跳转并溯源到原始日志

### 2020-12-30

 - Qradar user guide学习

### 2020-12-31

 - SAE bugfix: 删除被历史任务引用的规则报错返回数据信息格式有误；被历史任务引用的搜索告警规则不允许删除；修改属性支持数组后校验规则是否更新逻辑。

### 2021-01-04

 - alg算法模块bugfix, log太多，磁盘空间被占满。猜测是logback依赖包版本有bug导致。修改为log4j，更新Jenkins job。
 - 规则支持按照安全信息组名称检索。

### 2021-01-05

 - not occur模板设计思路整理

### 2021-01-06

 - not occur模板设计讨论与方案确定
 - 测试support&bugfix(audit规则名称转义，搜索告警启停计入audit)，安全同事问题support(告警无法溯源，id不在告警sim模型里)

### 2021-01-07

 - not occur模板设计讨论与方案确定
 - 测试support&bugfix(audit规则名称转义，搜索告警启停计入audit)，安全同事问题support(告警无法溯源，id不在告警sim模型里)

### 2021-01-08

 - not occur模板实现开发

### 2021-01-11

 - not occur模板实现开发(template, 规则生成，sae-core not occur核心处理逻辑)
 - not occur模板实现wiki整理：http://gitlab.hansight.net/root/enterprise-document/wikis/design/sae-not-occur-template-design
 - ndr direction_key生成逻辑修改，增加alarm_name

### 2021-01-12

 - sae-core not occur模板规则加载、trigger listener处理，生成告警、历史任务；功能自测

### 2021-01-13

 - Qradar rule response limit功能调研

### 2021-01-14

 - esper output rate limit功能调研，发现不适合sae场景，无法配置输出数量，无法根据分组字段值做limit

### 2021-01-15

 - sae告警输出限流功能设计方案思考与整理

### 2021-01-18

 - sae告警输出限流功能设计方案重构(之前考虑采用滚动时间窗口，发现滚动窗口存在问题，改用滑动时间窗口)

### 2021-01-19~20

 - sae告警输出限流功能cache与redis性能对比测试(利用其过期配置功能，使用告警id作为key，统计未过期的key的数量，判断是否达到阈值，实现需求)，测试发现，在size为10万的情况下，两个性能都很差；使用令牌桶RateLimter方式也存在问题，鉴于令牌是一定速率生成的，下个告警过来时，令牌如果尚未生成，就存在告警丢失/延迟输出的情况。讨论后决定，不采用Qradar(响应不超过x次每x时间每x)，改为静默期方式，多长时间内只允许生成一个告警，分组条件仍保留。
 - follow-by模板规则，关联条件使用contain规则配置

### 2021-01-21

 - 态势感知7.0版本搜索告警bugfix，分组字段规则，时间差小于时间窗口长度时，如果es聚合结果为空，会陷入死循环
 - 基于hotfix-5.5版本做sae-core定制，direction_key可配置，脱离zookeeper依赖，走单机运行模式
 - sae告警response limit功能开发

### 2021-01-22

 - 基于hotfix-5.5版本做ice定制，根据attack_direction重置告警的direction_key
 - sae告警输出限流功能测试
 - 分析模块930版本明文密码加密(分支：brain1.0-password-encrypt)

### 2021-01-25

 - sae告警输出限流功能测试
 - sae告警输出限流功能设计wiki整理：http://gitlab.hansight.net/root/enterprise-document/wikis/design/sae-response-limit-design
 - 分级分布式场景sae资产丰富化epl编译加载报错bugfix(assetEnrich的事件参数不识别，改为*)

### 2021-01-26

 - sae&ice规则回滚及召回功能讨论与开发
 - 运营环境ndr告警direction_key改为merge_key，相同merge_key的生成同一个安全事件

### 2021-01-27

 - sae&ice规则回滚及召回功能开发

### 2021-01-28

 - sae&ice规则回滚及召回功能开发
 - 告警attack_direction字段值改为数组

### 2021-01-29

 - sae&ice规则回滚及召回功能讨论与开发

### 2021-02-01

 - sae&ice规则回滚及召回功能开发(sae使用内部事件的规则需要同步保留生成该内部事件的规则)
 - not-occur模板自测及提测
 - ice direction_key修改为数组后存在bug(beta版本中存在)，问题定位，强制类型转换抛异常(cache中保存的是JsonArray，强转为set时抛异常)

### 2021-02-02

 - sae&ice规则回滚及召回功能自测
 - 告警response limit功能提测
 - 内测环境告警无法正常生成原因分析

### 2021-02-03

 - not-occur模板实现逻辑及为何要设置分组测试同事TOI
 - sae not occur模板问题分析及解决思路探索(日志都是A事件，但连续两个A的时间间隔已超出timeWindow情况，这种情况下也需要生成告警。但当前的做法，在epl中已经更新了内存中lastA的时间了，导致isNotOccur自定义函数时间检查结果为false，无法生成告警)。想到的方法是当该笔数据满足lastA过滤条件，同时又应该触发告警时，先将该数据暂存，待trigger监听器中将满足条件的数据取出后，再更新到内存。

### 2021-02-04

 - sae&ice规则导入预览及导入接口增加delete字段(删除的规则名称列表)
 - sae not occur模板bugfix

### 2021-02-05

 - 告警response limit功能bugfix，redis checkExpire和set分两步做，没有使用原子性操作，而dispatcher是多线程处理的，存在并发问题，导致告警多输出了。
 - 安全同事support，not-followby场景，规则配置有问题，告警输出太多。场景不适合用该模板实现，建议使用not-occur。

### 2021-02-07

 - 规则删除导入逻辑bugfix，区分运营环境及客户环境，删除时，运营环境改规则名称，置位logic_delete，清除配置内容；导入时，对于置位logic_delete的规则优先做处理，防止检查无效导致规则无法删除。
 - not_occur模板功能及response limit功能合入dev。
 - 规则标签功能开发：告警输出规则标签数组；支持多个标签值查询(mapper foreach实现)

### 2021-02-08

 - 规则标签功能自测，合入dev

### 2021-02-09

 - 规则回滚召回功能合入dev

### 2021-02-20

 - bugfix: 带distinct的having count模板功能失效，epl不对，分析原因是代码合入时解决冲突有误，导致epl生成错误。
 - bugfix: 根据ip relation计算攻击方向时抛空指针异常，导致告警无direction_key。分析原因是内网ip不存在，objectCheck返回null，false || null时抛异常。加了一个optical check。

### 2021-02-22

 - bugfix: not occur模板告警输出逻辑重构，用户配置了输出字段时，使用各个分组中的最近一笔日志的字段值作为输出字段
 - bugfix: response limit失效。分析代码来看，dispatcher代码有问题，不清楚是不是该问题导致的，暂时修复了这部分代码，测试目前正常。

### 2021-02-23

 - 数据分析各个模块多语言支持，furion/alg已完成，ice还在改。
 - 信息安全部环境，一规则针对某事件的具体ip不生成告警，执行历史任务后发现，该事件的其他ip是可以正常输出告警的，唯独该ip不可以，猜测并最终定位到是全局白名单的影响导致。

### 2021-02-24

 - 数据分析ice模块多语言支持。
 - ice规则配置文档整理。

### 2021-02-25

 - 分级部署模式下规则下发功能实现思路
 - 搜索告警子任务数据表针对每个规则做更新操作。

### 2021-02-26

 - 分级部署模式下规则下发功能实现思路文档整理与功能开发

### 2021-03-01

 - 分级部署模式下规则下发功能开发

### 2021-03-02

 - 分级部署模式下规则下发功能debug，提测
 - 分析各个模块i18n message更新整理，生成excel


### 2021-03-03

 - 分析模块多语言问题bugfix
 - 分析模块sae/alg es升级support

### 2021-03-04

 - 分析模块ice es升级support

### 2021-03-05

 - ice重构代码学习, refactor, buffer/engine/process_chain...

### 2021-03-08

 - ice重构代码学习
 - 多语言既有中英文message整理

### 2021-03-09

 - 建行HA angler bugfix：启动时会删除job_data中的数据重建任务，但job_data表id是自增的，会导致主机备机id不一致，HA有问题，暂时把删除job_data部分代码移除
 - 多语言support系统语言代码优化，从配置文件中移除，改为从db中读取
 - es升级ice-web部分代码修改，metaData key有问题，是固定的，索引修改后部分查询不生效(安全事件history)，key改为对应es index索引前缀。

### 2021-03-10

 - 建行HA sae-monitor启动失败原因分析：zookeeper版本与程序中不一致，导致curator调用方法创建节点抛异常。
 - sae搜索告警支持规则下发功能。修改了消息通知部分代码及规则下发逻辑：消息通知放在一个函数中来做；页面规则下发处理(调用函数实现)和consumer接收父节点规则消息处理走不同逻辑(消息处理完毕后将消息进一步发给下一级子节点)。

### 2021-03-11

 - sae规则下发bugfix，合入dev分支
 - 搜索告警代码review，找寻可以优化的点

### 2021-03-12

 - 搜索告警代码优化：子任务保存在es中的结果每天定时清理
 - 百胜不告警问题回复
 - 安全事件历史任务相关索引改动，以history_开头

### 2021-03-15

 - 太平环境sae不出告警问题support(确定环境部署，规则配置，数据是否满足条件(follow-by规则，过滤条件，日志时间))

### 2021-03-16

 - 太平环境sae不出告警问题support，定位到是乱序导致的follow-by规则无效。

### 2021-03-17

 - i18n英文部分message更新
 - sae规则页面添加一个配置项，“静默ICE默认策略”，当这个配置项开启时，告警将不对ICE默认规则生效
 - bugfix: 内容包导入验证时没有滤掉规则的多维度相关属性，导致导入时提示某些多维度属性不存在的警告。在规则验证时已滤除这些字段。

### 2021-03-18

 - 百胜不告警问题分析：数据不满足条件，无法生成告警

### 2021-03-19

 - 太平5.5hotfix，follow-by规则不生成告警，增加前置正序器，解决事件乱序问题

### 2021-03-22

 - ice安全事件溯源原始日志查不到bugfix，datasource table里面存储了不同的source对应的es index，ice-web最初的实现代码将source和index混淆成一个了。已修复，提交测试；
 - sae规则配置错误response进一步细化，提示安全同事是哪边的错误导致的。目前整理出模板、事件源、过滤条件、关联条件、规则编译失败相关的几类错误。

### 2021-03-23

 - sae规则配置错误response进一步细化
 - ice导入规则后静默ICE默认策略不生效问题bugfix，sae规则消息只处理了一部分。
 
### 2021-03-24

 - 算法模块问题分析，sae规则repsonse错误问题分析；
 - 看书：数据存储与检索
 
### 2021-03-25

 - 太平follow-by规则不生成告警问题；
 - 客户现场本脑版本eps低原因分析，最终定位到时一个正则部分匹配的信息组太复杂导致，关掉引用该信息组的规则后，正常；
 
### 2021-03-26

 - 护网，sae问题及排查思路文档整理

### 2021-03-29

 - i18n 更新，合入330 dev build
 - 护网，sae问题及排查思路文档细化
 - 太平问题support，两个sae-core，性能很差，不停full gc，patch中添加statement metrics接口，便于排查问题。

### 2021-03-30

 - 护网，sae问题及排查思路文档更新至wiki

### 2021-03-31

 - i18n message 更新
 - 太平问题support，整一个build，脱离zookeeper依赖

### 2021-04-01

 - 应急部护网现场sae处理速度慢问题定位；三峡护网现场sae模块异常问题定位
 - 太平问题support；百胜告警无法正常生成问题定位(现场lag有几千万甚至上亿级别，猜测是lag过大导致数据还没来得及消费就丢失了)，暂时关闭了几个耗时较大的规则。

### 2021-04-02

 - ice-web去除org.apache.pdfbox依赖，使用的2.0.22版本存在cve漏洞

### 2021-04-06

 - i18n message更新
 - 建行护网support，定位慢规则(规则引用了多个正则belong、rlike)

### 2021-04-07

 - 太平hotfix，follow-by模板优化，涉及三个及以上事件时，对关联条件拆分，分别放入对应的事件中作为过滤条件。
 - 农行需求讨论

### 2021-04-08~9

 - 太平hotfix，follow-by模板优化，涉及三个及以上事件时，对关联条件拆分，分别放入对应的事件中作为过滤条件，协助测试
 - 护网support
 - 农行需求讨论，决策引擎实现方案确定

### 2021-04-12

 -  农行基线需求

### 2021-04-13~14

 -  太平hotfix，follow-by问题不出告警分析support
 -  人行上报迁移1.5GM版本support

### 2021-04-15

 -  太平hotfix，follow-by问题不出告警分析support，定位到是由于我们对pattern的subExpression有10w的限制，现场有其他两条规则的相关计数和已达到该上限，数据直接丢弃，无法新生成subExpression，导致这个follow-by的规则无法正常生成告警，目前该问题无法解决，暂时只能调大限制。
 -  人行上报迁移1.5GM版本support
 -  护网威胁情报规则配置support
 -  not-occur模板规则优化

### 2021-04-16

 -  人行上报迁移1.5GM版本support
 -  农行基线需求讨论与方案确定

### 2021-04-19

 -  农行基线需求的实现思路整理

### 2021-04-20

 -  农行POC细化方案讨论，改用搜索告警实现；前端页面改动、数据结构改动

### 2021-04-21

 - brain1.5升级，告警sim不存在原因分析&bugfix
 - 学习es聚合，编写样例，为后续农行基线需求开发做准备

### 2021-04-22

 - 农行基线需求开发，整理框架和代码编写思路

### 2021-04-23

 - 基线计算功能开发，采用date histogram方式求动态基线

### 2021-04-25

 - date histogram、terms分组都是bucket聚合，得知es query bucket数量受限后，重构基线计算方法，根据interval分段求值，不再采用histogram。

### 2021-04-26

 - 基线分析，告警生成功能开发

### 2021-04-27~28

 - 基线分析功能自测

### 2021-04-29~30

 - 基线分析功能合入农行poc分支；
 - 整理农行poc测试方案

### 2021-05-07

 - 基线功能合入农行poc分支后自测；
 - 基线功能wiki整理

### 2021-05-08

 - 农行poc分支test support
 - 太平5.5环境未生成告警问题support

### 2021-05-10~12

 - 农行poc分支test support
 - esper configuration event type配置学习，后面如果属性字段允许配置多级嵌套的话，可以通过添加子类型的方式实现，这样，可以在epl语句中可以直接采用.连接属性
 - 5.13~5.16在天津出差，参加政企安全大会

### 2021-05-17

 - 搜索告警问题定位，规则reload后无法创建job；cron部分位置的值有限制，比如分钟，range为[0,59]，当调度周期为60min时导致cron错误，misc将定时任务删除，无法调度。第一个问题已fix，第二个暂时记了一个case，后面考虑怎么优化搜索告警这一块。

### 2021-05-18~19

 - HA方案
 - not-occur模板规则优化

### 2021-05-24

 - not-occur模板规则优化，弃用定时器，改用treemap

### 2021-05-25

 - IPV6调研

### 2021-05-26

 - not-occur模板treeMap性能测试有些问题，具体实现细节讨论
 - 多语言分支合入dev

### 2021-05-27

 - not-occur模板treeMap 1000个分组时性能问题原因定位，我测试的场景是1个事件过来，会触发1000个分组都生成告警，在trigger中更新treeMap时，一下子将1000个分组值添加到treeMap的key(value为hashset，addAll方式)中，耗时较长。正常不会出现这种情况，重新做了测试，还是1000个分组，分别测试每次触发生成1/10/100/200个告警情况下的eps，结果如下：
1 trigger：eps: 30w
10 trigger：eps: 23.5w
100 trigger：eps: 4.3w
200 trigger：eps: 2.5w
 - 太平实时监控页面eps为0问题定位：sae-core metrics一直有统计，但重启后metricbeat中的sae-core sock文件与sae-core真实的sock文件不匹配，导致sae-core一直hang在socket accept函数上，metricbeat由于sock文件错误拿不到sae-core的实时eps数据，导致实时监控页面有问题。

### 2021-05-28

 - not-occur模板按1000:1生成告警性能测试，eps大概35w
 - not-occur模板bugfix，遍历map时调用map.remove抛ConcurrentModificationException
 - com.github.seancfoley，ipaddress lib学习

### 2021-05-31

 - ip工具类性能测试，多个零散ip，测试tireTree性能，比当前我们使用的性能要高。
 - 全局白名单生成告警需求分析，讨论认为对统计类、关联分析类规则有影响，暂时不做。
 - sae护网复盘新需求：规则列表展示规则更新时间、近7天告警数量(不交给sae-monitor实现，防止多引入1个jar包，改由调用智能分析接口实现)
 - sae测试问题support，并发导致sae告警有问题，暂时没定位到原因
```
 (EngineExceptionHandler.java:23) - rule name:zx-having-sum测试（无分组条件） rule epl:[SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, ti_dimension,  WINDOW(id) AS _WINDOW_ID, WINDOW(event_id) AS _WINDOW_IDS, WINDOW(src_address) AS _WINDOW_ENRICH_SIP, WINDOW(src_address_array) AS _WINDOW_ENRICH_SIPS, WINDOW(dst_address) AS _WINDOW_ENRICH_DIP, WINDOW(dst_address_array) AS _WINDOW_ENRICH_DIPS, WINDOW(data_source) AS _WINDOW_ENRICH_DATASOURCE, WINDOW(data_source_array) AS _WINDOW_ENRICH_DATASOURCES, WINDOW(client_host_sign) AS _WINDOW_ENRICH_HOST, WINDOW(client_host_sign_array) AS _WINDOW_ENRICH_HOSTS, WINDOW(attack_id) AS _WINDOW_ENRICH_ATTCK, WINDOW(attack_id_array) AS _WINDOW_ENRICH_ATTCKS FROM GlobalEvent(node_chain_tag is null AND ( spin_tag = 0L AND ( belongs(`src_address`,'R41176V50085')))).win:ext_timed(occur_time,10 sec)  AS A HAVING (sum(A.`src_port`) >= 3306)], event info: {"dst_address":"192.168.1.5","dev_address":"172.16.101.169","malware_detection_engine":"kpave","domain_name":"domain1","event_type":"/-1/G1CYSXJW001f/ND2ZURFW005a/W1SPW7AP005c","occur_time":1622449177024,"rule_name_list":["test_zx_new"],"spin_tag":0,"src_address":"172.16.101.160","id":"400150895891841024","vulnerability_id":"CVE-2019-3439","rule_name":"test_zx_new","receive_time":1622449177024,"collector_source":"zx_172.16.101.169","@nbf_state_785":"No A, ActiveTime=1622449169998, EventTime=1622449177024","url":"http://zx.com","data_source":"360EDR","sim_name":"web攻击告警","src_port":3306,"rule_id":"8289fd83-9c18-45af-80b5-65a9ed3372f2","sim_version":"3.1.0000","file_hash":"hash","dst_port":3399,"event_level":0,"event_name":"webshell上传"}, found an exception:java.lang.NullPointerException: null
 2021-05-31 15:36:34,332:WARN origin-alarm-processor (FurionProcess.java:530) - illegal alarm data: [zx_ice_in_slience] = {dst_address=192.168.1.1, end_time=1622446594320, data_source=360EDR, src_address=172.16.2.246, id=400140063246123008}. err info: missing start_time&end_time or unexpected data types
```

### 2021-06-01

 - qradar not occur场景试用版本调研
 - 本脑1.0版本运营环境搭建

### 2021-06-02

 - qradar 涉及资产的规则及资产管理模块试用版本调研(配合sae告警输出资产相关字段需求)
 - sae告警输出资产功能讨论，讨论后决定该功能暂时不做
 - sae 三个及以上事件时follow-by规则优化，关联条件限制and

### 2021-06-03

 - 建行HA测试问题support

### 2021-06-10

 - asia联调环境问题support，历史任务无法生成告警，后定位到是磁盘空间满了，es写入失败
 - SIM2.0相关文档

### 2021-06-11

 - 分析各模块依赖包整理
 - jira case整理
 - 金国性能测试support，单机模式下内部事件走kafka问题分析

### 2021-06-15

 - sae规则性能评估标准
 - esper **GPLv2协议**替代方案，暂定为drools
 - sae rule body整理，后面考虑改动，移除不必要字段
 - not occur性能测试support，采用**treeMap**之后，性能优化了很多

### 2021-06-16

 - 金国测试环境单机模式下内部事件走kafka问题定位分析
 - sae sim2.0改造

### 2021-06-17

 - sae sim2.0改造，部分数据结构改动，规则生成逻辑改动

### 2021-06-18

 - sae sim2.0规则生成debug

### 2021-06-21

 - sae 跟sim2.0相关的一些接口调整
 - sae规则导入优化，只更新缓存与db不符的规则

### 2021-06-22

 - ice sim2.0适配
 - 建行规则状态变更后，几个sae-core加载不同步问题定位(停止规则后，备份的sae-core能接收到规则变动消息，但调用core接口时发现规则还在加载着，并没有移除；开启规则类似)。最终定位到是HA的问题，规则改动后，数据还没同步到备份的节点，sae-core收到更新消息后读取db，拿到的还是老数据。修改方法：改动sae-core mysql连接配置，优先连接主节点数据库。
 - HA方案学习

### 2021-06-23

 - sae规则语法调整，字符串统一使用"..."，字段统一使用`...`
 - 建行搜索告警问题，规则已停止，job_data数据表中仍存在(代码bug，已存在时没有拿到job_id，导致停止/删除规则的时候无法正常删除job)
 - nacos方案学习

### 2021-06-24

 - nacos HA方案讨论
 - sim2.0, 删除属性、删除实体、删除实体关联的属性对规则的影响接口调整，增加两个接口

### 2021-06-25

 - nacos 服务发现

### 2021-06-28

 - sim2.0 关联分析规则改动，搜索告警数据结构变化、规则生成逻辑、添加/更新/导入接口检查逻辑、移除实体/属性影响规则逻辑修改
 - angler模块HA feat: 基于nacos配置管理及服务发现功能实现es-proxy自动加载&切换

### 2021-06-29

- 百胜安全事件处置后仍有告警合入问题定位
- angler模块HA feat debug

### 2021-06-30

 - angler模块HA功能log4j配置不生效问题定位，调试对比ice启动过程发现，log4j配置放到nacos服务器时，angler程序启动时没有加载FileLoader，导致找不到classpath下的log4j，只能加载默认的springboot里的，导致log输出有问题；目前只能将log4j配置放到本地，来解决这个问题。
 - sae-monitor支持从nacos服务器读取配置，正常启动，服务发现功能不用我做

### 2021-07-01

 - sim2.0 sae功能验证&bugfix
 - angler bugfix，代码发现了两个问题(规则更新问题(没必要检查状态是否更新)，filter语句生成问题)
 - 确认：搜索告警，全局事件情况下不检查过滤条件是否为空

### 2021-07-02

 - sim2.0 给安全同事演示sim2.0各个功能

### 2021-07-05

 - 关联分析规则sim2.0实体不作为过滤条件
 - 农行poc搜索告警增加sum基线分析功能

### 2021-07-06~07

 - 农行poc搜索告警基线分析输出基线参考值及阈值信息(参考值默认10条，可配置)，当前，参考值提取部分放在了获取当前结果之后，没有等检查完该数据是否要生成告警后再提取，不太合理，**后面需要做优化**。
 - 目前在农行poc环境做了简单测试，效果还可以，并没有做详细测试。

### 2021-07-08

 - sim2.0关联分析规则配置改造，约定页面默认不配置告警开始时间结束时间，后端自动生成
 - HA，分析这边与job_data表关联的url修改，ip:port改为对应服务名(涉及angler和sae-monitor历史任务)

### 2021-07-09

 - esper pattern语法review，新模板A followed by B and not C可行性

### 2021-07-12

 - 新模板A followed by B and not C语法讨论
 - sae规则创建/更新response优化，指明具体的问题点(什么事件名称/属性有问题)

### 2021-07-13

 - sim2.0 sae、ice影响字段整理，目前已知domain_name->domain，威胁情报和白名单匹配字段需要修改。
 - sae规则字段梳理，为后面平台化做准备

### 2021-07-14

 - 平台化feat，sae规则字段梳理(移除部分字段)
 - 建行6.0beta现场问题support，都是enqueue失败的日志，而且sae有重启过，入队失败是sae处理速度跟不上导致，重启猜测是内存占用率过高导致。目前定位并调整了几个慢规则。
 - 平台化功能开发：规则部分字段给出默认值，接口不需要传递(frequency)

### 2021-07-15

 - 平台化功能开发：Highlevel规则crud接口，复用本脑接口
 - 安全事件打分逻辑：目前存在bug，运维已提单

### 2021-07-16

 - sim2.0字段改动：
 request_msg不存在，url类型的白名单改为http_url_path
 net_protocol不存在，确认删除
 user_account不存在，确认删除
 漏洞利用，url移除，改为http_url_path
 威胁情报匹配，url移除，改为http_url_path，$\color{Red} {看下sae规则是否需要修改} $
 需确认下ice那边用到的一些字段，是否需要移除或添加到属性表中

### 2021-07-19

 - 平台化改造：lowlevel epl规则创建/修改/查询接口实现，删除和启停复用老接口
 epl规则没有跟sae规则放到一个数据表中，而是单独建了一个表来存储

### 2021-07-20

 - 平台化改造：lowlevel epl规则接口调试；历史任务接口复用。
 - sim2.0测试case review

### 2021-07-21

 - sim2.0测试case评审后改动，增加事件修改影响规则的接口；可根据实体搜索规则
 - angler、sae-monitor HA 配置文件改动，公共配置使用nacos配置
 - 平台化改造：单机模式下sae-core加载epl规则，生成告警

### 2021-07-22

 - 平台化功能自测，包括sae-monitor 规则增删改查、历史任务接口及sae-core功能

### 2021-07-23

 - 平台化SAE接口文档整理：[E:\Projects\360本地安全大脑\平台化-sae-support\关联分析引擎平台化API接口文档.md][1]
[wiki][2]
  [1]: E:%5CProjects%5C360%E6%9C%AC%E5%9C%B0%E5%AE%89%E5%85%A8%E5%A4%A7%E8%84%91%5C%E5%B9%B3%E5%8F%B0%E5%8C%96-sae-support%5C%E5%85%B3%E8%81%94%E5%88%86%E6%9E%90%E5%BC%95%E6%93%8E%E5%B9%B3%E5%8F%B0%E5%8C%96API%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.md
  [2]: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=20124935

### 2021-07-26

 - 【护网反馈需求】SAE功能增强:搜索告警增加阈值区间功能开发(普通聚合操作符、同比本期阈值操作符都添加属于/不属于区间判断逻辑)，目前做法是修改告警使能判断逻辑，不用操作符实现Comparable接口实现，改用guava range来做。对于max/min聚合类型，修改了下溯源逻辑，只给出一个溯源日志id。后面需要验证一下这两部分。

### 2021-07-27

 - 【护网反馈需求】SAE功能增强:规则里可以配置源地址为受害者组，目的地址为攻击者组(目前的做法是：告警输出中增加一个勾选框配置是否反转攻击角色，文字描述为 “勾选后源地址为受害者，目的地址为攻击者”，如果勾选了，则将其转成一个标记属性格式。属性名称就叫攻击角色反转，attr_field是attacker_reverse，整形)，流式分析检索分析都支持这个配置。
 - HA测试bugfix: angler启动失败问题；unicode编码导致线上配置文件中文乱码(目前将中文的部分移至线下)

### 2021-07-28

 - SAE功能增强：in操作符除支持ip外，额外添加数组类型字符串支持，元素支持string/ip/整形，demo:
 事件名称 in ["web访问","网络连接"]
 ip in ["1.1.1.1","2.2.2.2"]
 源端口 in [8080,443]
 当前的做法是将字符串转成jsonArray，判断里面的数据元素是否是同一类型，根据类型进一步封装，使用esper自带的in操作符判断。

### 2021-07-29

 - 近期做的功能文档整理
 - jira提测功能bugfix

### 2021-07-30

 - sae功能增强部分(攻击角色反转、检索分析增加区间判断功能)自测
 - 平台化测试环境问题讨论
 - HA功能提测

### 2021-08-02

 - sim2.0 sae bugfix(根据实体模糊搜索sae规则，实体防在raw json中，在mapper中用->获取json字段不正常，一直报错，将>转义或换成CDATA方式都不正常)，后使用JSON_EXTRACT(raw,'$.entities')方式解决，sql语法是'select id from sae_rule where raw->'$.entities' like '%entity%' limit 1;'。mapper.xml与sql语法有差异，后面注意。
 - HA测试方案讨论
 - 平台化部分功能测试，与杜鹃讨论。

### 2021-08-05

 - 农行基线功能合入dev

### 2021-08-06

 - HA功能增强：使用jedis连接redis哨兵(不再使用spring-data-redis(springboot 1版本不支持哨兵密码加密)，替换为Jedis，并兼容sentinel加密)，读取redis数据方面变动较多，尤其是watchlist部分，后面需重点测试一下
 - sim2.0功能，支持根据实体名称搜索规则，支持多选并模糊匹配，多个之间是与的关系
 - 农发行威胁情报类规则不生成告警问题support，规则配置错误，使用Domain匹配事件，但过滤条件是源地址match

### 2021-08-09

 - sim2.0功能合入dev分支，冲突解决；ice配置文件更新
 - 参与SIM2.0的测试进展会议
 
### 2021-08-10

 - dev改动合入HA分支，HA模式下不支持sae-core单机运行方式，epl规则在HA模式下支持duplicate模式加载，支持通过url指定及消除指定加载的sae。
 - HA测试研讨会

### 2021-08-11~12

 - 建行having count规则告警问题分析，having count模板，以xff地址为分组，count>=50即生成告警。客户生成环境现场，8.10 16:00~16:30，跑历史任务，生成的告警数量很少，有些时间段应该可以生成告警的，但都没有生成。通过创建规则并打开audit，在建行定制化环境中发送事件，复现了这个问题，跟本脑版本做对比，最终定位到了问题原因。
 - 当前，建行生产环境中sae的日志每天量都很多，基本上是入队失败的日志，应该不少日志都没有进入引擎分析。漏报还是可能的。后面需要进一步定位慢规则。

### 2021-08-13

 -  建行内容包导入测试环境
 -  SAE规则与HQlite使用语法不统一问题说明
 -  jira case处理

### 2021-08-16

 -  sae epl规则重复告警问题分析：最终定位发现，debug页面展示出来的重复告警，其中有一个是内部事件，内部事件触发了epl规则，trigger中获取的eventBean的underLying实际上就是内部事件对象，后续对这个对象的改动导致了内部事件的数据的变动，最终反映到debug页面。修复的话，改动trigger，依据underLying新生成一个map。
 -  建行内容包sae规则分析

### 2021-08-17

 -  建行内容包sae慢规则分析整理
 -  jira case处理

### 2021-08-18~20

 - jira case处理，自己看东西

### 2021-08-23

 - 规则增加计数接口，包括所有的、开启的、未启动的
 - 内容包环境数据库alarm_key更新，全部改为空，走默认场景merge_key生成逻辑

### 2021-08-24

 - arthas build合入sae-core build
 - angler HA问题，nacos连接不上导致程序启动失败，但supervisord仍认为程序是运行状态
 - 建行问题support

### 2021-08-25

 - angler HA问题，nacos连接不上导致程序启动失败，但supervisord仍认为程序是运行状态，查看进程运行状态后发现，angler虽然启动报错，但程序并没有异常退出，导致supervisord认为进程仍处于running状态。启动报错属于RuntimeException，在main方法里尝试捕获该异常并退出，解决此问题。
 - 建行问题support，昨天下午又复现了24号的问题，下午告警量较之前减少很多，鉴于24号创建的规则已关闭，不是那几个规则的原因，根据之前已调研得到的现场慢规则，分析现场的数据发现，那几条慢规则对性能影响很大，建议调整。

### 2021-08-26

 - 建行问题邮件回复
 - 调整sae-monitor eventBase接口，事件增加威胁类型、情报类型字段，数组类型(数据表查询sql很复杂)
 - IPAddress lib调研，计划明天开始做这部分

### 2021-08-27

 - 资产字段调整，sim2.0内容包中数组字段isArray字段已恢复正常，去除了sae-monitor那边的数组字段配置。
 - 对搜索告警启动规则数量做限制，最多启动100个，目前，对add/update/control/import接口做了改造。
 - 东航sae升级到本脑1.5版本，规则导入问题support，问题情况是大量规则都无法正常导入，显示过滤条件有问题，customize_internal_ip6这个字段不能用于belong操作符，查了下这个字段在属性表里被定义为内网IP，只能将这个字段换了个名称，重新导入了下内容包，规则导入恢复正常。环境中用到了很多belong 内网IP的操作，之前6.0版本并没有对belong右操作数做严格检查，导致出现错误，之前的版本这些规则应该无法正常工作。

### 2021-08-30

 - IPAddress类信息组匹配性能对比测试，性能测试发现用该lib和当前我们的ip二分查找搜索逻辑性能差别不大，暂时不修改ip匹配这部分
 - 优化数字类信息组匹配逻辑，类似ip信息组匹配

### 2021-08-31

 - 建行规则优化逻辑答疑
 - 东航belong内网IP不生效问题support，定位出来是代码bug，本脑1.0版本1.5版本存在同样的问题，已在hotfix分支修复。

### 2021-09-01

 - 建行ice改动，发送到第三方soar的kafka数据结构调整

### 2021-09-02

 - 移除sae-monitor消息处理耗时统计部分功能(废弃代码，当时只是为了调试用的)
 - 限制搜索告警规则启动数量功能开发

### 2021-09-03

 -  建行问题support，龙御waf规则数据处理抛异常(array element type mismatch)，最终定位到解析规则有问题，使得ipv6_array数据为string类型，而非string[]，导致esper window聚合抛异常

### 2021-09-06

 - sae bugfix：audit日志问题；jedis setIfAbsent功能
 - 建行问题support，eps大概五百，大量数据没有处理即丢弃；sae-core每天定时零点重启，明天继续

### 2021-09-07

 - 建行问题support，从sae启动参数，运行时间，jstat查看gc情况，epl metrics情况等方面分别分析，给出了总结和建议。

### 2021-09-08-09

 - 资产改动影响ice修改：ice打分逻辑，资产影响因素采用资产的分数；通知策略组部分，资产相关的过滤条件匹配改动，初始时将资产数据放入缓存，匹配时直接拿缓存数据做匹配，不再去查询es，减轻对es的压力，提高处理速度。

### 2021-09-10

 - sae问题排查wiki整理，分为本脑前版本和本脑版本。对本脑sae debug页面使用也做了说明。

### 2021-09-13~15

 - ice debug使用加入wiki

### 2021-09-16

 - sae规则、watchlist、ice规则导出功能后端加入audit日志，使用AOP实现该功能。

### 2021-09-23

 - 测试，评估es忽略大小写影响对分析这边的影响(es  mapping并不是所有的字符类型属性都是忽略大小写的，下拉的属性保持大小写敏感)：
sae实时和历史任务都没有影响。但sae只有like、rlike及belong正则类信息组是忽略大小写的，其他操作符及belong字符串比较类信息组都是大小写敏感的。es忽略大小写之后，两边匹配结果仍旧不能完全同步。
可能导致的问题：利用过滤条件搜索到的日志可能会变多，历史任务耗时更大；客户现场sae实时告警无法正常生成，拿过滤条件搜索日志时能搜到，但告警出不来，可能质疑引擎的处理能力。
angler规则如果配置了过滤条件，根据过滤条件得到的聚合值可能不准确。
如果字段在es mapping中配置了忽略大小写，terms聚合后key都转为小写；如果字段在es mapping中没有配置忽略大小写，terms聚合后key保持不变。

### 2021-09-24

 - support平台化接口文档review

### 2021-09-27

 - sae多级部署，打开metric，聚合类规则抛array element mismatch异常分析与bugfix，参考http://jira.b.qihoo.net/browse/LCBRAINDEV-1888，定位发现，如果数据字段与esper语法不一致，在聚合时会抛出该异常(比如src_address_array是String[]，但数据中是String)
 - 安全同事support，1.5版本环境告警无法正常生成原因分析
 - 2.0内容包环境，sae规则id有些与1.5版本规则id不一致

### 2021-09-30

 - esper pattern subExpression数量限制放入配置文件，默认100000
 - 测试那边发现问题，资产多维度规则存在时，esper处理抛出并发异常，参考http://jira.b.qihoo.net/browse/LCBRAINDEV-1952。定位到是资产多维度规则匹配时会对原有数据做修改(添加了src_asset_dimension、dst_asset_dimension)。多个引擎并发处理同一笔数据时会导致并发问题。**目前该问题不在930修复**，如果客户现场报问题，可采用修改配置文件中esper引擎数量、打patch来解决。
 - 在定位上面问题时发现，自定义函数如果抛异常，直接
 - 自测发现问题，规则equals方法有问题，导致每小时重新加载一次，带来的问题是影响规则状态，导致漏报。**该问题不在930修复，问题已解决，后面需测试**。

### 2021-10-08

 - 资产多维度规则存在时，esper处理抛出并发异常问题分析。
一开始考虑采用EPLMethodInvocationContext实现，把资产的数据放入规则statementInfo中，资产的其他过滤条件都是需要通过src_asset_dimension/dst_asset_dimension做cast/convertToArray转换的，将src_asset_dimension和dst_asset_dimension做成自定义函数，通过EPLMethodInvocationContext获取资产的字段，这样不会修改原始数据，资产数据直接放到规则上下文中，不会对其他规则造成影响。
但测试时发现问题，规则epl中assetEnrich是有用到资产字段时才会添加的，esper在编译epl过滤条件时，会将其编译成一个语法树，我无法控制assetEnrich操作都在其他过滤条件之前，比如：
```
资产.目的地址.重要性 exist, epl：assetEnrich(A,'dst_address',dst_address) and src_asset_dimension('importance') is not null
```
**测试下来，is not null在enrich之前，鉴于这会src_asset_dimension还是null，规则永远不匹配。这是一直存在的问题，只是之前没有发现。**
讨论后决定，在匹配资产相关的过滤条件时，直接取缓存中的资产数据做匹配，这样对性能也没什么影响。
sim2.0版本，威胁情报、资产、脆弱性的字段都是固定不变的，有考虑是否改为JavaBean，但字段过多，后面字段如果有改动又要改代码，还是放弃了。不过，资产维度和其他两个维度处理确实需要区分开来，其他两个维度的数据是shuri直接给的，资产的数据是sae自己获取的，后面考虑下如果修改epl。

### 2021-10-09

 - 资产多维度规则存在时，esper处理抛出并发异常问题修复：采用的方案是修改epl，资产数据在用到时从缓存中获取。
 - sae属性加载处理bugfix：esper语法会有规则id字段；属性没有变化时，定时reload也会触发。

### 2021-10-24

 - 农行distinct类基线逻辑修改：已更新到"农行基线分析"，逻辑还有些问题，后面dev分支需要修改。

### 2021-10-25

 - sae IPToLong函数优化，直接自定义函数，通过与操作完成，弃用lib接口和cache。

### 2021-10-26

 - 建行ice引擎启动失败问题support，定位到是我本地打包时把application.yml打包进去导致，本地是本脑2.0，引入了redis哨兵，ice使用的是jar包里的application.yml，连接哨兵失败，导致启动失败。
 - 运维客户现场5.0版本sae问题support，单机改分布式，sae启动失败。
 - splunk告警功能学习

### 2021-10-27

 - splunk告警功能学习

### 2021-10-28

 - splunk调研分享，wiki整理：http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22685878
 - HQLite和SAE语法差异点整理

### 2021-11-01

 - HQLite和SAE语法差异点整理，wiki: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22685172

### 2021-11-02

 - 搜索告警目前各种分析方式的计算方法文档整理，http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22687077
 - HQLite和SAE语法差异点整理review，讨论了下后面要做的东西

### 2021-11-03

 - ipv6 parse代码更新，性能测试，测试下来，比ipv4要慢一些。

### 2021-11-04

 - HQLite和SAE语法差异点讨论，整理todo list
 - SAE语法改动

### 2021-11-05

 - 百胜问题support，1个环境中sae-core.log正则匹配抛异常，eps很低，定位到是正则匹配导致的性能差，倚天更新hotfix-1.0，引入hyperscan匹配正则，我今天support验证功能，对比测试，出build给百胜(11.4重启后，eps在2k~6k之间，客户两次截图eps不一样，受当前分析的日志的影响)
 - 上午build出来后，下午运行一段时间后eps还是不高(刚换eps为4w，运行一段时间后1w多甚至出现8千多的情况)，猜测是正则语法写的不好导致，目前问他们要了下规则epl，改了点我认为可以优化的规则，后面修改一下看下情况

### 2021-11-08

 - 百胜问题support，定位慢规则，协助现场收集慢规则数据，尝试本地复现

### 2021-11-09

 - 利用收集数据，使用内存生成数据的方式，尝试本地复现。目前没有复现成功，只是看到字符串过长时，String.getBytes()方法耗时较大，暂记一个knonw issue。

### 2021-11-10

 - 脆弱性匹配问题、匹配逻辑讨论
 - 建行告警漏报问题support

### 2021-11-11~12

 - 安全同事反映一个过滤条件查询失败的问题，sae也存在同样的问题，定位是panther parse错误导致的，已让测试提bug，后面修好后先合入maintenance。
 - 脆弱性匹配功能开发
 - 建行告警漏报问题support，暂时给他们优化了一个规则配置，安全信息组内容修改了一下，后面如果还有性能问题需要想办法定位下慢规则

### 2021-11-15

 - 脆弱性匹配功能开发
 - 东航问题support，3个sae，每个加载四百多条规则，eps在3万左右，lag两三千万。

### 2021-11-16

 - 脆弱性匹配功能开发，规则epl生成，数据匹配逻辑

### 2021-11-17

 - 脆弱性匹配功能自测

### 2021-11-18

 - 规则epl语句生成类(HaliteTranslator)尝试修改，尝试了下，改动会比较大，逻辑基本不动，只是把function改为class实现，一个操作符对应一个类。不想改了，意义不大，只是可读性高一些。
 - ipv6功能开始开发，ipv6前缀转ipRange逻辑已做好。

### 2021-11-19

 - IPV6Range相关代码实现，用于处理belong匹配逻辑

### 2021-11-22

 - IPRange改用泛型类实现

### 2021-11-23

 - 建行问题support，对他们导出的8个当时观察的性能差的规则，给出了每个规则的优化思路

### 2021-11-24

 - 关系类操作符处理ip类型逻辑功能：一个ipv4，一个ipv6无法比较大小，直接返回null；相同类型的ip可以比较大小
 - ipv6全局白名单处理逻辑
 - 客户现场问题support，ARM平台环境，hyperscan的 Database类中在静态代码块中loadlib报ERROR，没有捕获，导致sae调用Database报错，引擎无法正常启动，已在2.0hotfix中修复该问题，客户现场验证通过，合入dev分支，记录case。

### 2021-11-25~26

 - 搜索告警支持ipv6，ice支持ipv6

### 2021-11-29

 - ice-web支持ipv6，artifact支持ipv6，两者都是用了判断是否是内网IP的功能

### 2021-11-30

 - hql转epl语法翻译部分代码重构，每个操作符一个类，类重写toEpl方法，构造操作符对应的epl语句；在处理之前，需要对hql表达式做校验，并对左右操作数做重构(主要针对威胁情报、资产字段)

### 2021-12-01

 - hql转epl语法翻译部分代码重构
 - 分析各模块mysql8.0更新改动support，system变为mysql保留字，sql中对该字段做转义

### 2021-12-02

 - 脆弱性匹配bugfix，没有考虑左值为普通字段，右值为脆弱性字段的情况，>/>=/</<=/like/rlike/contain这些操作符逻辑要改动。代码合入dev。

### 2021-12-03

 - sae历史任务对接HQLite2.0，不再使用es搜索，改用hqlite2.0实现功能开发：hqlite模块服务发现；调用hql接口实现过滤条件hql1.0转hql2.0语法。

### 2021-12-06

 - 建行问题support：
  - 告警下发到soar延迟问题
    原因：incident下发告警到soar之前会查询该告警关联的原始日志，但是原始日志较多查询比较慢，因此导致数据堆积发送到 soar 延迟
    解决方案：将 incident 查询原始日志的索引名称改为一个不存在的索引，这样就不存在查询原始日志较慢的问题，告警可实时下发到soar
  - 关闭规则依然告警问题
    原因：实时的和历史的都是连的同一个es，告警都写入同一个es了。实时的页面上看到的那些告警实际上都是历史的那台机器产生的。
    解决方案：目前已将历史引擎的所有规则关闭，避免历史和实时引擎告警混淆。未来历史引擎这边可以通过跑历史任务来验证规则。

### 2021-12-07~08

 - sae历史任务对接HQLite2.0，hqlite2.0语法学习

### 2021-12-09

 - 告警合并策略重构方案讨论

### 2021-12-10

 - 告警合并功能开发
 - apache log4j规则rlike不生成告警原因分析

### 2021-12-13

 - 告警合并功能开发，epl中输出威胁可信度，分级部署模式该功能存在问题：如果输出属性为数组类型，则保存关联日志中该字段出现过的所有值
 - apache log4j规则rlike不生成告警原因分析

### 2021-12-14

 - 告警合并功能开发，搞定epl语法，包括输出威胁可信度，数组类型字段输出所有关联事件的属性

### 2021-12-15

 - 告警合并功能开发，any-order模板、not-occur模板规则调试后输出威胁可信度改动，epl语句中不带威胁可信度，统一在监听器中处理。
 - 安全同事提出的bugfix: any-order模板如果删除事件后再添加新事件，无法正常输出新事件的属性。
 - 威胁情报可信度配置放入Alert实体，不在db中新增字段，方便规则升级。默认输出日志中的最大值。

### 2021-12-16

 - 合并告警功能开发：esper监听器数据处理代码优化;合并字段生成时，如果包含告警名称/内容/处置建议，需滤除其中的数组字段;not-occur模板、any-order模板bugfix：如果输出属性为数组类型，需输出所有事件的对应属性值。

### 2021-12-17

 - 合并告警功能开发：新建告警业务实体对象，添加告警相关字段到该实体；给测试讲解功能及主要测试点，生成测试所需内容包。

### 2021-12-20

 - 合并告警功能开发：搜索告警支持自定义告警合并字段，支持输出数组，输出标记值

### 2021-12-21

 - 北京本脑产品部support，edr告警规则无效问题support，溯源发现日志是edr打点数据，不匹配规则，了解了下，云端告警的情况是 系统会把edr打点日志送到云端，也会送给sae，云端规则匹配产生告警日志 然后将云端告警日志送到本脑，id跟这个打点日志是一样的，这个云端告警日志触发规则，生成了告警。云端告警日志在日志查询页面看不到，看到的是最初的打点日志，所以日志的内容不能匹配。云端告警日志搜索：选择高级搜索，index == "edr-alarm" | where id == "xxx"
 - sae/ice规则导出加的审计日志功能提交到hotfix-brain1.5分支
 - 删除/更新/手动创建安全事件；添加/删除关联分析历史任务；添加/删除安全场景任务这几个接口加一个auditMsg，hotfix-brain1.5、hotfix-brain2.0还有dev都提交

### 2021-12-22

 - 合并告警功能开发：sae告警输出攻击者类型/受害者类型，这两个字段为枚举类型，已更新至安装脚本。

### 2021-12-23

 - 合并告警功能开发及bugfix，之前alarm_name等字段引用属性使用matcher实现，发现matcher存在线程安全问题，修复
 - 监听攻击场景reload消息，防止攻击场景导入后引擎中攻击场景缓存无法更新，后面攻击场景改为走安装脚本

### 2021-12-29

 - 攻击者类型、受害者类型移除账号类型
 - sae告警输出规则使用的关联分析模板类型
 - 国网1.5 maintainence分支sae/ice审计日志改动合入
 - 告警输出威胁情报相关字段信息；输出字段可配置。威胁情报目前存在问题：如果引用多个事件，只能取最后一个事件引用的威胁情报做输出，没有做合并。
 - mysql升级到8版本

### 2021-12-30

 - 关联分析规则分享ppt整理及分享
 - 安装脚本攻击场景数据表问题修改，赋值错误，导致scene_tyoe字段不是edr/ndr攻击场景
 - 国网1.5 maintainence分支sae/ice审计日志功能自测

### 2021-12-31

 - sae告警/内部事件输出威胁可信度，如果日志不存在该字段，设置为未知
 - esper监听器数据处理代码优化review&bugfix

### 2022-1-4

 - sae功能自测，发现威胁情报/资产维度匹配有问题，目前，非数组类型是通过cast强转来实现过滤匹配的，数组类型是通过convertToArray实现的，cast目前没有问题，但如果升级时字段类型有变就有问题了(倚天担心数据处理会抛异常)；convertToArray使用的时候，整数类型 in 数组 会有问题，威胁情报的话可以给esper新建一个eventType，ti_dimension使用那个eventType来实现，这样使用时直接ti_dimension.xxx就可以了，资产这块不好做。

### 2022-1-6

 - 客户现场2.0版本，belong 内网IP匹配错误问题定位，不是sae这边的问题，是security_intelligence和system_config这两张表内网ip不一致导致的；belong正则类信息组问题，sae正常，智能检索问题。
 - 建行6.0版本，ext_timed timeWindow时间窗口问题，告警开始时间结束时间时间差超过配置的时间窗口问题复现及分析。
 - esper cast强转debug，发现数据格式不对，不会抛异常，这样数据就不会丢掉从而导致别的规则无法正常触发。**多维度使用cast没有问题，只是如果字段类型有变化，需要更新对应规则。**

### 2022-1-7

 - 多维度匹配，in 整数数组问题bugfix: 最简单的方式，epl语句中整数加L后缀，整数L in (convertToArray(xxx))
 - 多维度匹配逻辑wiki整理

### 2022-1-10

 - 客户现场问题support，belong 内网IP不生效
 - ice规则导出，加审计日志

### 2022-1-11

 - sae-core 历史任务问题整理，目前没有好的解决思路
 - 信息安全部环境sae-core性能差原因分析，定位到是or-fb规则，A事件过滤条件中有用到正则，B事件量相当大，esper的实现逻辑是每个B都要走A的正则过滤，导致正则匹配膨胀了几百倍，导致sae性能很差，eps只有不到五千。讨论优化方案是把关联条件提前到过滤条件前面，通过短路，减小过滤条件匹配的次数，提高性能。这个方案也有缺陷。

### 2022-1-12

 - 信息安全部关联类规则epl优化，关联条件提前到过滤条件前面
 - bugfix: merge_key提取字段有问题，导致merge_key字段不对
 - 广电客户现场问题support，6.0beta版本ice，安全事件处置后没有过期问题support，目前只是给出了个接口，调用接口手动过期安全事件。
 - 运维那边客户hotfix-1.5 sae-core patch

### 2022-1-13

 - bugfix: 不缓存内部事件，直接查db获取。
 - 规则生成优化，补全规则的开始时间结束时间输出时，对内部事件做特殊处理，告警的开始时间取内部事件的开始时间，告警的结束时间取内部事件的结束时间。

### 2022-1-14

 - 自己看了点腾讯云es的资料：https://cloud.tencent.com/developer/column/4008/tag-10307

### 2022-1-17

 - 通知策略组不生效bugfix：review代码时发现，如果规则没有配置输出源地址目的地址，普通模板、nbf、nfb规则没有输出这些字段，告警的源地址组目的地址组数据不完整，安全事件的内外网信息不全，影响安全事件逻辑。
 - 告警输出规则名称字段，sae_rule_name(多级部署时，无法通过sae_rule_id得到关联分析规则名称)

### 2022-1-18

 - 腾讯云 es wiki: https://cloud.tencent.com/developer/column/4008/tag-10307
 - 日志易数据能否被sae引擎处理分析，结果是可以，但有些问题：事件都没有事件名称；字段与AISA解析不一致，有些字段我们系统没有，字段类型也不完全一致。

### 2022-1-19

 - bugfix: not-before模板、not-occur模板过滤条件结果为null时数据处理抛空指针异常，导致数据丢失
 - 现场问题support，or-follow-by模板，15s，有一个ip没有生成告警原因分析(另一个ip正常)，最终定位到是dv队列满了，数据没发到kafka，调大dv内存后，数据发出来了，但告警仍旧没有生成，最终没有定位到原因。

### 2022-1-20

 - 现场问题support，window聚合失败，看字段没什么问题，怀疑是修改过window聚合字段的属性类型，重启后问题解决。
 - 【SAE-CORE】FollowBy规则命中大量A后，可能导致B规则的过滤条件被重复执行，进而导致性能问题分析: http://jira.b.qihoo.net/browse/LCBRAINDEV-2885, 分析来看，pattern类规则都存在这个问题，lookup? 每个A都会过滤一遍B，A数量超多。暂定的解决办法是正则由自定义函数实现。

### 2022-1-21

 - 农行问题support，dv给的数据有问题，规则已被修改，之前epl已获取不到，后面继续观察
 - 吉利客户现场问题support，ice规则触发生成多个安全事件。原因，规则关联条件中有一个值为null，导致告警数据无法合入

### 2022-1-24

 - 农行问题support，告警误报，最终通过audit日志的api记录，定位到是规则20号改动，filter语句有问题导致的。部署方式 != 灰度 攻击结果=攻击成功  这两个中间没有and，导致没有对攻击结果做限制。这是前端的一个bug，已提出让前端修复。
 - 威胁情报类规则不告警问题support，2.1版本威胁情报增加ti_source字段，这个字段非必须，这样导致规则配置ti_source!=xxx时，因为该字段为null，导致不满足条件，无法生成告警，已通知安全team修改内容包规则。

### 2022-1-26

 - 吉利客户现场问题support，告警不生成高级场景安全事件，最终通过es audit索引定位到是ice规则改动过，改动之前并非引用的那个sae规则，而那个sae规则是静默ice默认策略的。
 - sae bugfix: 告警输出攻击场景子类型alarm_type字段，否则影响安全事件详情页面合并告警卡片展示(根据该字段决定卡片列表字段)

### 2022-1-28

 - 规则引用内部事件溯源规则链接口开发
 - 执行历史任务时，如果规则引用内部事件，需将所有生成该内部事件的规则一并找出来再执行。

### 2022-2-10

 - [SAE]增加调试接口，指明规则引用事件链；历史任务规则引用内部事件，需附带生成内部事件的规则功能自测

### 2022-2-11

 - 【信息安全部】sae-core引擎处理状态已经异常，但集群自监控仍然显示正常问题分析，为代码bug，SaeMetrics中max kafka lag没有赋值，导致monitor规则无效

### 2022-2-14

 - 更新monitor模块sae的数据异常检测规则，连续5次引擎没有没有检测到异常数据，恢复正常状态。
 - es ip匹配逻辑：ipv4地址与ipv6地址比较时，会将ipv4转成兼容ipv4的ipv6地址，再与ipv6的地址做比较。

### 2022-2-15

 - pattern类规则，等待时间窗口放大(默认增加3min延迟时间，可自行修改配置)，保证告警正常生成

### 2022-2-16

 - 中央国债bugfix: sae-core没有加载globalMapping信息，导致规则名称/告警内容等引用有映射的字段时无法正确映射输出。已在hotfix-2.0及dev版本修复

### 2022-2-17

 - angler加载globalMapping信息，正确输出告警相关字段
 - 信息安全部环境，sae分布式扩容

### 2022-2-18

 - SAE增加调试接口，指明规则引用事件链；历史任务规则引用内部事件，需附带生成内部事件的规则功能合入dev及农行分支；
 - 动态信息组历史任务不使能

### 2022-2-21

 - sae-core配置文件更新，kafka相关配置(consumer&producer&topic部分)重新整理，修改相关代码

### 2022-2-22

 - sae-core配置文件中kafka相关配置(consumer&producer&topic部分)整理重构；内部事件单独发往固定topic，由dv写入es，sae消费内部事件topic(集群模式下level-2引擎不消费)功能开发&自测。

### 2022-2-23

 - 性能测试发现了like操作符的性能问题(目前使用StringUtils.containsIgnoreCase实现，本地eps只有20w，换用String自身的toUpperCase后contains，eps能达到70w)，暂时记一下，最近想下优化方案。

### 2022-2-24

 - 浙江电力定制：关联分析规则增加规则用途字段定制功能开发，usage约定：通用0，平时1，战时2
 - 东航客户现场support，需求暂时没办法满足，想要实现的场景是某个事件的数量小于某个值时触发告警。规则有配置分组，满足条件的数据最近几天一直没有。
   关联分析规则不行；统计类规则过滤条件不满足bucket返回结果为空，也不满足。

### 2022-2-25

 - like字符串忽略大小写各种算法调研(String.contains(网传jvm执行时做了优化)、KMP、BM、RK)等，及性能测试，忽略大小写(转大写后比较、转小写后比较)，得出结论是String.contains性能最高，耗时主要集中在忽略大小写这块，contains性能很高。

### 2022-2-28

 - like字符串忽略大小写优化，跟宋倚天讨论过之后，做些折中，自己依据String.index算法实现，字符大小写比较自己实现，对忽略大小写的字符做些限制，部分字符(比如汉语拼音等共977个)不支持忽略大小写匹配。

### 2022-3-01

 - like字符串忽略大小写优化性能测试
 - 农行需求：历史任务增加是否更新动态信息配置

### 2022-3-02

 - 农行需求：历史任务增加是否更新动态信息功能开发&自测
 - 修改sae硬编码字段，适配江苏网信办标准字段

### 2022-3-03

 - 修改ice硬编码字段，适配江苏网信办标准字段

### 2022-3-04

 - 修改artfact硬编码字段，适配江苏网信办标准字段

### 2022-3-07~08

 - 搜集文档，了解springboot版本升级这块，大致理清升级思路：
   gradle升级；springboot升级；影响其他依赖jar包版本(es等)；配置文件更新；编译语法错误；
```
gradle cmd
./gradlew clean --refresh-dependencies
./gradlew dependencies >d.log
./gradlew dependencyInsight --configuration compile --dependency elasticsearch --warning-mode all
./gradlew clean build
```

### 2022-3-09

 - artifact/sae-core/angler springboot版本升级，本来想升级到2.6.4，但我们现在用的nacos依赖的springboot版本为2.3版本，2.4版本nacos config(0.2.10版本nacos，https://github.com/nacos-group/nacos-spring-boot-project/issues/159)运行有问题，最终确定springboot版本升级到2.3.10。spring-core该版本有问题，升级至

### 2022-3-10~15

 - ice springboot版本升级
   common包问题：bootJar.enabled=false, jar.enabled=true，否则导致编译失败
   注解问题：需要被springboot识别(@Target, @Retention)，否则注解无效
   log问题：nacos导致，放入本地配置文件中，不放到nacos配置中心，否则无效。
   @PropertySource问题：暂未解决

### 2022-3-16

 - 信息安全部告警溯源不正确问题，最终定位到是2.1版本的bug，已在hotfix分支上修复，并更新环境build
 - dev环境sae-monitor接口response乱码问题分析，最终定位到是springboot版本升级，contentMessage转换导致的。已修复。

### 2022-3-17

 - ice springboot版本升级，分析模块springboot升级合入江苏网信办分支
 - 江苏网信办环境问题check&fix，geo相关字段改动

### 2022-3-18

 - 江苏网信办环境分析模块测试
 - 江苏网信办字段check

### 2022-3-19~21

 - 农行规则不生成告警问题分析：发一笔数据可以正常生成告警，说明引擎没有问题；发大量相同数据时告警数量不对，最终定位到是or-follow-by规则subExpression数量已达上限导致的(时间窗口1h)。已跟他们沟通说明原因并告知减小时间窗口长度。

### 2022-3-22~25

 - 一体机那边精准告警的功能support，告警输出log_vendor字段
 - 分析模块es接口整理(农行需求)

### 2022-3-28

 - 升级springboot版本后@PropertySource注解无效问题bugfix
 - 一体机问题support

### 2022-3-29

 - 一体机问题support
 - 农行规则patternStatement subExpression数量过大问题support，数量限制可配置移入农行分支；增加配置项，延长FB/OR-FB/RU pattern类规则时间窗口等待时间移入农行分支
 - 一线安全分析本脑问题support(安全事件数组大小有限制，导致部分数据没有合入安全事件相关字段)

### 2022-3-30

 - 规则引用事件链接口返回数据格式调整，合入dev&农行分支
 - 农行问题support，监控页面ice报接收告警延迟过高警告，定位原因是收到的告警数据与当前时间相比超过两小时，日志接收时间与发生时间相差超过2小时导致

### 2022-4-01

 - 宁波银行客户现场问题support，ndr场景，默认ice策略，在外部扫描器探测的场景下，同一源地址会进行多次攻击，触发不同目的地址的相同告警，本身只是一个事件，但是以目的地址聚合，就是N个事件。暂时让他们用高级场景规避了这个问题，并告知安全同事。

### 2022-4-02

 - hotfix-2.1 support

### 2022-4-06

 - 客户问题support，规则不匹配，但日志查询能查到，定位到是日志搜索与sae规则=操作符匹配字符串大小写有区别导致的。问题在于es定义的analyzer是忽略大小写的。
 - 农行新模板需求support，having字段分组匹配计数满足条件触发，分析需求、设计实现思路并自测，该功能可实现。
 - 建行内部事件id字段有问题，导致event_count计数不对，event_id数组包含无效id bugfix。
 - 信息安全部sae-monitor kafka log报错问题调查，定位是system_node数据表kafka server配置不对导致。

### 2022-4-07~09

 - 建行新需求support，告警输出phy_system_cname字段。

### 2022-4-11~12

 - 农行支持按网络区域分组统计、按ip所属网络区域计数数量满足条件的定制功能调研

### 2022-4-13

 - 农行定制功能开发：
   修改sae-monitor distinct模板，支持用表达式分组和having；
   sae-core嵌套ip匹配功能逻辑实现

### 2022-4-14

 - 农行定制功能开发：sae-core加载嵌套ip数据，构建匹配数据集

### 2022-4-18

 - 农行定制功能开发：sae-core加载嵌套ip数据，构建匹配数据集(continued)

### 2022-4-19

 - 农行定制功能开发：sae-core加载嵌套ip数据，构建匹配数据集(continued)，响应add/edit/delete/reload消息，更新后同步至CollectionCenter，既支持belong，也支持按网络区域分组groupBy

### 2022-4-20

 - 国产达梦数据库适配
 - 信息安全部环境问题support，告警误报，读取log，发现加载该规则的sae-core出问题了，后台日志不停报错((IndexTreeBuilder.java:187) - .removeFromNode (92) Could not find the filterCallback to be removed within the supplied node)，已记录至客户现场问题排查记录，后面有空看下，暂时重启sae-core规避了这个问题。

### 2022-4-21

 - sae模块国产达梦数据库适配

### 2022-4-22

 - ice、artifacts模块国产达梦数据库适配
 - 20号信息安全部环境问题.removeFromNode warning log分析，目前没有定位到具体原因

### 2022-4-24~5

 - 20号信息安全部环境问题.removeFromNode warning log分析，猜测是并发导致的问题，也看到规则reload时有数据并发异常出现，目前没有复现成功
 - 江苏网信办环境问题告警不生成support：规则配置有问题，大部分规则都是威胁情报相关规则，但事件名称不对；shuri那边字段修改没有改全
 - 430 patch问题分析，sae出现好些CocurrentModificationException，猜测是not_before模板修改数据导致的问题。

### 2022-4-26

 - 430 patch sae CocurrentModificationException bugfix， 合入dev
 - 20号信息安全部环境问题.removeFromNode warning log分析，目前没有思路

### 2022-4-27

 - 一体机SAE规则新增silent模式、XDR模型规则需求了解及问题整理

### 2022-4-28

 - 中央国债any-order模板规则创建失败问题bugfix：分组字段超过两个时epl语句有问题，已修复并合入dev/hotfix-2.0/hotfix-2.1分支
 - 信息安全部ice问题查看，磁盘空间不足，rocksdb cache无法写入，安全事件生成即丢弃，ice运行不正常
 - not-occur模板功能逻辑农行客户解释
 - 一体机SAE规则新增silent模式、XDR模型规则需求讨论

### 2022-4-29

 - 一体机SAE规则新增silent模式、XDR模型需求功能开发：sae-monitor增删改查support

### 2022-5-05

 - 分析三个模块ipv6功能合入dev，解决冲突

### 2022-5-06

 - 一体机SAE规则新增silent模式、XDR模型需求功能开发：sae-monitor增删改查、导入导出逻辑

### 2022-5-07

 - 一体机SAE规则新增silent模式、XDR模型需求功能开发：sae-core性能监控逻辑实现思路思考及整理
 - 信息安全部攻防演练support：告警数量较之前偏少，没有发现原因，sae功能正常，但消费数据量比只有es当天数据量的一半，猜测是全局白名单命中较多导致(解析错误等原因数据量不多)

### 2022-5-10

 - 一体机SAE规则新增silent模式、XDR模型需求功能开发：sae-core性能监控逻辑实现
 - 军队项目文档support：检测分析中心模块(sae-monitor、ice-web)单元测试用例整理

### 2022-5-11

 - 军队项目文档support：检测分析中心模块(sae-monitor、ice-web)UML类图、类及方法设计说明
 - 一体机SAE规则新增silent模式、XDR模型需求功能sae-monitor接口改动，告警阶段告警级别支持多选搜索，支持查询并编辑所有不可见规则(xdr，silent)

### 2022-5-12

 - 一体机SAE规则新增silent模式、XDR模型需求功能开发：angler性能监控逻辑实现，build已更新至一体机环境准备下周联调

### 2022-5-13

 - 安全同事support，http响应报文中带响应body，根据http响应报文格式，响应头部和响应正文会有一个空行(\r\n)，给出解决方案 like "\r\n\r\n"，包含连续两个\r\n表示带body的。在规则配置过程中发现了epl转换的错误，代码对epl做简化时将连续的空白字符转为一个空格，这样会可能会修改规则语句，已在dev分支上修复。

### 2022-5-16

 - LSE同事support，定位延迟告警
 - ice代码走读
 - 国产化平台sae-core问题分析：kafka告警发不出去，导致数据流处理的各个线程阻塞，引擎无法正常工作

### 2022-5-17

 - silent&xdr功能联调
 - ice代码走读
 - 信息安全部旁路分析设计思路support，相关规则(count模板时间窗口1d)告警漏报问题support

### 2022-5-18

 - silent功能ice代码联调
 - 安全同事旁路分析设计support

### 2022-5-19

 - 告警过滤需求讨论

### 2022-5-20

 - 信息安全部环境，检索分析规则不生成告警原因分析，misc调用有问题
 - 农行support，佃权sae代码解读，后面做多维度关联分析功能
 - 国产化适配测试环境，sae问题分析及bugfix
 - 告警过滤功能开发

### 2022-5-23

 - 告警过滤功能开发：数据结构定义、ice-web增删改查接口、规则转换、数据表操作

### 2022-5-24

 - 告警过滤功能开发：ice-web hql语句转换

### 2022-5-25

 - 告警过滤功能开发：ice-web hql语句转换，规则监控逻辑；incident功能开发：processNode, alarmEngine

### 2022-5-26

 - 告警过滤功能开发：alarmEngine引擎过滤功能开发

### 2022-5-27

 - 告警过滤功能开发：ice告警过滤规则变动消息处理

### 2022-5-30

 - 搭建告警过滤功能自测环境
 - xdr模型，规则引用信息组模型校验(xdr/siem)

### 2022-5-31

 - 告警过滤功能联调+自测，可以提测了
 - silent规则导入测试问题：客户环境silent规则更新后是否用内容包规则覆盖，明天讨论。
 - 一体机xdr安全事件测试，告警不生成问题分析：最终定位是被告警精准过滤配置过滤了，页面查询不到。

### 2022-6-01

 - silent规则导入更新逻辑改动：客户端通过内容包/cps导入时，对于silent规则，不管规则有没有改动过，直接更新；客户端通过页面导入时，不给出提示让用户选择覆盖或跳过，直接更新；如果规则已改为非silent模式，不做更新或删除。内容包更新时不复用旧规则的启停状态。

### 2022-6-02

 - silent规则导入更新test support
 - XDR全流程梳理

### 2022-6-06

 - 建行下发到第三方SOAR告警增加user_name字段
 - 告警过滤功能提测
 - XDR全流程梳理：确认各个环境有没有问题

### 2022-6-07

 - XDR数据源接入：神经元类型讨论、soar应用联动处理讨论
 - support安全同事配置XDR模型规则
 - 农行问题support

### 2022-6-08

 - XDR内置数据源接入安全同事协助配置

### 2022-6-09

 - 一体机XDR数据源模型改造，新增子分类建设，内置神经元类型及对应内置数据源梳理，采集类型整理
 - 一体机新增hash类威胁情报匹配逻辑
 - 告警过滤功能合入dev分支及一体机dev分支

### 2022-6-13

 - 一体机XDR相关的应用联动，添加内置预案(封禁解封ip/域名/主机/md5)
 - 日志审计问题support(ice、sae)
 - 告警过滤功能bugfix
 - 客户现场问题support，not-before模板告警误报问题分析(事件无序导致)

### 2022-6-14

 - 一体机XDR数据源接入页面增加两个接口：获取神经元类型关联数据源状态；主动启动神经元类型关联数据源
 - 信息安全部定制化：搜索告警触发逻辑改造需求讨论：要求只要数量达标就告警，不需要达到时间窗口
 - 信息安全部环境一普通模板告警误报问题分析，暂未定位到具体原因

### 2022-6-15

 - 信息安全部环境一普通模板告警误报问题分析，使用arthas watch分析kafka producer输出的告警，定位到确实是告警误报了，但定位不到具体的原因，引擎加载的规则epl也是正确的。先重启了sae，后面看是否会复现。
 - 搜索告警触发逻辑改造需求讨论，区分分析类型、聚合类型，规则添加配置项；后面需考虑有分组情况下根据不同分组是否生成告警，时间窗口推进的长度不一致是否可实现。
 - 农行定制分支nacos开启服务鉴权功能
 - 农行定制需求：支持按网络区域分组统计、distinct模板改造(支持按ip所属网络区域做计数统计，数量满足条件即触发)的定制功能合入农行定制dev分支

### 2022-6-16

 - 云端一体化环境问题support，协议字段被改动，导致很多规则加载失败
 - 安全同事规则配置support
 - 信息安全部搜索告警改造实现方案讨论，改为滑动窗口，之前的做法有问题，已当前点为基准，往前查一个时间窗口长度的数据，而不是以之前定义的runTime为基准，以该值与当前时间的时间差为窗口做计算。
 - 信息安全部环境带ti_dimension的关联类告警异常原因分析及bugfix
 - 一体机优化点梳理

### 2022-6-17

 - 一体机优化点专项改动check及任务安排
 - 本脑xdr安全事件设计讨论

### 2022-6-20

 - 一体机630版本反馈问题汇总文档的讨论与理解
 - 一体机ice bug review & resolve

### 2022-6-21

 - 一体机ice bug review & resolve
 - 一体机添加告警及安全事件相关的soar预案

### 2022-6-22

 - 一体机ice bug review & resolve

### 2022-6-23

 - 一体机ice bug review & resolve
 - 一体机xdr安全事件处理逻辑代码走读

### 2022-6-27~29

 - 建行SAE积压问题support：
 引擎&规则优化：
 1. ip转数值方法优化
 2. ip类信息组匹配优化：规则中用到了大量的belong ip类信息组匹配，修改后性能应该有所提升
 3. like操作符性能优化
 4. 规则分析，给出规则优化建议(rlike、belong，多个rlike正则整合，表达式顺序调整)

### 2022-6-30

 - 一体机sae silent模式规则功能&xdr规则功能合入dev
 - soar应用联动study

### 2022-7-01

 - 信息安全部搜索告警逻辑改动
 - soar应用联动study

### 2022-7-04~05

 - 云阵对接soar应用联动脚本编写&联调，联调过程中发现了soar预案传参的bug，已通知王营

### 2022-7-11

 - bugfix: 本脑silent告警未写入正确索引
 - 邮储银行定制化support：contain操作符支持左右操作数均为数组，只要两个数组交集非空即可匹配。这是临时解决方案，本脑2.5版本考虑新增一些数组类操作符。

### 2022-7-12

 - 安全同事邮储银行定制化验证support
 - 信息安全部环境搜索告警问题调研，其中一个是angler的bug，已修复并合入dev分支
 - 一体机demo环境准备

### 2022-7-13

 - 安全同事邮储银行客户现场问题分析：前端+meta问题
 - 一体机demo环境XDR数据准备，跟安全同事一块，整理了三个场景，两个xdr的，一个siem的

### 2022-7-14

 - 一体机demo环境XDR数据准备，目前一共四个场景，三个xdr的，一个siem的
 - 一体机L3.5版本培训

### 2022-7-15

 - 一体机L3.5版本易用性问题反馈wiki review
 - 一体机demo环境XDR安全事件进程树绘制问题分析，定位为版本bug，已解决，更新至dev&lb-dev
 - 新城周会

### 2022-7-18

 - 一体机L3.5版本易用性问题讨论整理
 - 一体机demo环境数据构造
 - 建行sae积压问题support

### 2022-7-19

 - 一体机3.5版本demo环境数据review，demo环境数据构造完成，今天已发布
 - 本脑dev kafka消费数据问题bugfix:本脑2.5版本dv会把所有数据都发到kafka，sae要丢弃key带discard前缀的。内部事件及shuri发过来的日志不带key，sae处理时报空指针异常
 - 信息安全部搜索告警支持告警静默功能开发

### 2022-7-20

 - 信息安全部搜索告警支持告警静默功能自测，合入dev
 - 本脑xdr安全场景模型ice rule功能开发

### 2022-7-21

 - 本脑xdr安全场景模型ice rule功能开发
 - 本脑双子星模式规则下发逻辑改动&wiki整理

### 2022-7-22

 - 本脑xdr安全场景模型ice rule页面改造及接口对接
 - 本脑双子星模式规则下发逻辑测试项梳理

### 2022-7-25

 - 本脑xdr安全场景模型ice rule接口联调
 - 信息安全部搜索告警模块一group by规则告警漏报原因分析，同一批查询，部分数据生成了告警，个别几个分组没有生成。从log来看，满足条件应该触发，但告警没有生成，排除ice原因，log也没有报错，暂时修改build，多打点log，明天看情况。
 - 百胜客户现场问题support，一节点eps低，lag大，arthas分析是like操作符的原因，定位规则为log4j的内置规则，暂时先关了规则。

### 2022-7-26

 - 信息安全部搜索告警模块一group by规则告警漏报原因分析，更新了环境build(多加了点log输出)，遗漏的告警实际上有调用kafka producer接口发出，但实际上kafka并没有发出来。分析数据，都是固定的几个ip有这个问题，从规则及数据来看，规则的威胁特征列表引用威胁特征字段输出。对比其他ip的数据，那几个数据的威胁特征值特别长，一笔数据几万个字节。规则为统计类规则，count > 10输出，生成的告警body体相当大。修改规则(引用别的字段)后，告警可以正常输出。建议：改kafka producer配置；解析后的宙合的数据中威胁特征字段值=HTTP请求内容，这个是不合理的，建议他们修改数据格式。
 - 信息安全部安全事件攻击链路图为空原因分析，暂时未定位到原因，看ice-web的日志，通过es relation索引没有拿到安全事件对应的告警id。实际上relation索引里数据是存在的。后面需要再分析。

### 2022-7-27

 - 农行护网support：慢规则定位，通过分析线程栈、arthas watch，定位到"Apache Log4j2远程代码执行漏洞”规则性能比较差，用了多个like，版本还是用的StringUtils.containsIgnoreCase实现。暂时停掉了规则。
 - 一体机xdr神经元接入，重启按钮逻辑bug修复(重启会启动所有它关联的采集器，而非已有子类型的)
 - xdr安全事件详情2.5版本页面改动review

### 2022-7-28

 - xdr安全事件详情2.5版本页面改动sae适配改动，告警需输出合并所用字段，告警类型，规则触发相关的配置信息(只针对流式规则，依分析场景输出内容不同)。
 - 农行护网support：中午时一个线程栈查看时大都在Array.set处，后倚天猜测可能是not-occur/any-order模板的group-by自定义函数处理那块。我本地尝试复现，在对应函数处打断点，断点确实进入了。本地写了规则模拟数据发送，测试规则性能，发现不满足条件时eps可达上百万，但满足条件后eps很低，只有几千。问金国要了个机器，建规则发数据，用arthas分析线程栈，重现了现场的情况。目前知道现场有10条该模板规则。
 - 农行护网support：晚饭那会142节点eps降低，lag几百万，帮助现场用arthas分析，定位到还是like的问题，暂时建议现场把相关规则转到其他节点，平衡一下。目前发现有问题的规则都在该节点。

### 2022-7-29

 - xdr安全事件详情2.5版本页面改动sae适配改动测试
 - 百胜客户现场目前16w eps，sae lag很大，看了下都是like操作符的问题，暂时给他们出了个patch(基于2.1-hotfix，把like优化放上去了)，周一换下build，看下运行效果。

### 2022-8-01

 - 2.5版本xdr安全事件改造，ice-web部分接口适配改动。像攻击链、删除安全事件等。目前，手动创建/添加至安全事件还没有改动，后面记得做。
 - 护网support，POST /service/extdirect  HTTP/1.1，安全同事定位到是通过tomcat的这个接口发过来的，但是没找到相关tomcat日志，es增加了一个service的索引。我看了下2.1版本没有这个接口，尝试本地复现，404。搜索网上信息，这个是nexus的一个漏洞(CVE-2019-7238)，但我们只用它来做repo管理，暂不清楚原因。

### 2022-8-02

 - 天津信创一体机support
 - Qradar user guide(rule perfermance, asset management)
 - 性能测试support，当前规则数量差不多一千，后面还得想想怎么优化引擎，从规则配置层面也好，从匹配逻辑也好

### 2022-8-03

 - 一体机被动资产发现相关需求调研，流量和终端的数据拉通、整合，流量和终端的关联技术调研

### 2022-8-04

 - 运维客户现场support，有两个2.0版本客户现场，因资产数量过多导致ice性能不足，给现场打了patch；一个6.0版本现场暂时未定位到问题，需进一步分析。
 - 一体机需求讨论

### 2022-8-05

 - ASIA流量日志分析
 - 新城一体机周会

### 2022-8-08

 - 本脑sae模块es搜索由scroll改为search_after，自测
 - 运维support，本脑测试suppport
 - 一体机被动资产发现需求方案调研

### 2022-8-09

 - 一体机被动资产发现需求方案调研整理

### 2022-8-10

 - 一体机被动资产发现设计方案讨论

### 2022-8-11

 - 一体机被动资产发现设计方案细化
 - ice告警过滤增加inmap、not_inmap算子支持

### 2022-8-12

 - artifact代码走读

### 2022-8-15

 - 建行support，sae/angler/incident springboot版本升级至2.7.2

### 2022-8-16

 - 建行support，sae/angler/incident springboot版本升级至2.7.2，build及更新文档整理
 - 告警输出事件名称组
 - 参与一体机资产优化评审会议

### 2022-8-17

 - 一体机告警通知功能开发

### 2022-8-18

 - 一体机告警通知功能开发

### 2022-8-19

 - 分析各模块ipv6功能合入农行分支

### 2022-8-22

 - 一体机被动资产发现功能开发
 - 日志审计环境安全事件不生成问题support

### 2022-8-23

 - 一体机被动资产发现功能开发
 - 本脑inmap操作符bugfix，数值类多维信息组配置有问题
 - 百胜问题support，sae脆弱性数据读取异常，从错误日志来看，脆弱性数据有问题，相同字段的数据，不同记录的格式不统一，有的是string类型，有的是double类型，导致的这个问题。

### 2022-8-24

 - 一体机被动资产发现功能开发
 - 中央国债sae patch build，like性能优化代码合入

### 2022-8-25

 - 建行support，sae/angler/incident依赖包版本升级，修复漏洞
 - 属性增加alarm_source告警来源字段，目前指定五种类型(SIEM/XDR/AI/UEBA/CLOUD)，sae告警输出该字段。

### 2022-8-29

 - 了解本脑UEBA优化改造，一体机后面要引入
 ```
 目前了解到的功能：
 数据解析新增BDR/NTA数据源、场景建设；
 UEBA安全事件会展示在本脑安全事件列表中，详情页面与ice安全事件不同；
 整合本脑安全运营流程：告警处理、工单流程、数据分权；
 智能检索页面下，增加"UEBA原始告警搜索"功能；
 本脑智能建设页面下，会增加"合并告警搜索"功能；
 UEBA 合并告警-等同于本脑安全事件，es index: ueba_anomaly_incidents
 UEBA 原始告警-等同于本脑合并告警, es index: ueba_anomaly_alerts
 一体机与本脑的区别点是一体机也要提供接口，把UEBA的原始告警拿过来，在合并告警列表中展示。
 ```
 - 碧桂园项目support，规则用not 源地址 match做匹配，不合理
 - 本脑bugfix

### 2022-8-30

 - 碧桂园项目support
 - 本脑UEBA优化改造continue，理清UEBA逻辑

### 2022-8-31

 - 一体机借鉴本脑UEBA优化改造方案wiki整理，风险点&todo list
 - 资产解除失陷标记功能开发：解除失陷的逻辑是：打失陷的告警被处置完成。目前采用的方法是处置告警时，同步发消息给资产模块，资产模块检查该ip是否属于资产，相关ip的合并告警是否都处置完成，如果是，则调用artifact接口将自动失陷状态标记为正常。该方案需修改资产模块和artifact模块

### 2022-9-01

 - 资产解除失陷标记功能开发

### 2022-9-02

 - 本脑sae相关bug修复

### 2022-9-05

 - sae、artifact模块dev代码合入一体机分支
 - 信息安全部sae不生成告警问题support，有个sae运行不正常

### 2022-9-06

 - ice模块dev代码合入一体机分支
 - 信息安全部sae不生成告警问题support，两个sae环境给sae分配的内存只有12G。214环境sae不停的在full gc，每次都要耗费20多秒，好些follow-by/or-follow-by规则A事件都大几万，这个引擎基本上工作一小会就出问题了。227的sae不时地检测到nacos instanceChange事件，规则不停加载删除，工作也不正常。目前已更新了sae的build，将like优化放进去了。

### 2022-9-07

 - ice模块dev代码合入一体机分支，to be continued

### 2022-9-08

 - Building block学习
 - monitor模块sae epl问题support，规则表达的是连续五次引擎异常数据量为0，则消除警告。但epl编译报warning，规则语法使用follow-by every[repeat] (a and not b)。为了过滤是同一个引擎，过滤条件中有引用a和b的字段，导致了编译警告，测试了下规则语句，也是无效的。了解了下match_recognize语法，改用match_recognize实现该逻辑。

### 2022-9-09

 - SIEM + XDR 关系调整 需求讨论

### 2022-9-13

 - 一体机合入前端dev代码相关的功能&页面整理

### 2022-9-14

 - 一体机合入前端dev代码相关的功能&页面整理 to be continued, 输出文档
 - sae bugfix: 检查规则变化逻辑错误，导致规则定时reload
 - SIEM + XDR 关系调整相关工作梳理项中，安全事件/合并告警计算流程及数据结构调整改造

### 2022-9-15

 - 中央国债support: 规则链接口合入国债分支
 - 信息安全部环境，AISA数据分析，目前就流量和终端的数据整合，没有想到好的思路。AISA数据基本不带mac地址，协议都是应用层的。
 - 一体机support，lb-dev环境ice-web启动失败，没分析出原因，不清楚是机器问题； 失陷资产问题support。

### 2022-9-19

 - 合并告警策略对象化功能，API文档整理，增删改查导入导出接口开发

### 2022-9-20

 - 前端代码合入进度跟踪
 - 合并告警策略对象与规则互动部分改动
 - 合并告警策略支持内容包导入导出，增加内置3个合并策略；通知旁路分析开发同事改动

### 2022-9-21

 - 前端代码合入进度跟踪
 - 被动资产发现bugfix(修改es script脚本，使资产应用数据能够同步更新)
 - 一体机安全事件不生成问题bugfix
 - 告警通知功能合入一体机dev分支

### 2022-9-22

 - 前端代码合入进度跟踪
 - 一体机ice相关bugfix，配置文件中尽量不要携带${}相关字符串，引用时可能有问题
 - 本脑告警合并策略联调support，系统监控测试support

### 2022-9-23

 - 一体机分析模块代码合入；新版本优化建议

### 2022-9-26

 - 本脑自动化测试环境问题bugfix(运营规则feature引入)
 - 一体机测试环境check，前端代码合入进度跟踪

### 2022-9-27

 - 中央国债项目support，提供sae-monitor包，给出规则引用链build更新说明文档
 - 本脑运营规则使用信息组问题讨论与解决，之前的模式，XDR规则只能使用XDR和共用的信息组，SIEM规则只能使用SIEM和和共用的信息组。运营规则模式下，这种方式有问题。给出的解决方案是XDR规则可以使用所有的信息组。
 - 自动化测试环境问题bugfix(合并策略功能引入，合并策略消息变动没有监听，代码处理抛空指针异常，告警无法正常生成)
 - 一体机测试环境check，前端代码合入进度跟踪

### 2022-9-28

 - 信息安全部环境support，根据标签无法搜到检索分析规则，是已修复的一个bug，需要更新环境的sae-monitor build
 - 本脑测试support(规则导入问题，如何友好提示)
 - 一体机测试环境check，输出文档

### 2022-9-29

 - 周会，一体机support

### 2022-9-30

 - 一体机自动化测试结果分析
 - 本脑运维support(sae不停重启，没有定位到原因)
 - 本脑sae规则support，修改神经元对应的db的规则标签字段值

### 2022-10-08

 - 一体机相关：告警展示优化、告警高亮、UI问题；安全事件详情关联溯源bugfix

### 2022-10-09

 - 一体机相关
 - 百胜问题support，sae lag很大，各个partition消费不均衡，sae eps不高，从日志看，sae引擎性能没有问题。artifacts同样lag很大，状况跟sae类似。猜测是io或带宽问题，但停掉了sae同一机器上的shuri之后，sae eps没有上升。没定位到具体原因。下班前将topic删除了，明天继续关注这个问题。

### 2022-10-10

 - 一体机功能：更新部分攻击场景名称(影响sae及ice规则，整理update sql语句)，添加UEBA安全事件攻击场景；告警高亮显示讨论(不根据告警的scene_type来决定是ndr的还是edr的，改为依据日志的data_source来判断，data_source="360AISA"的是NDR，data_source="360EDR"的是EDR)
 - 一体机bugfix: 一个内网ip放入告警的外网ip实体bug分析，定位出不是ice的问题。
 - ueba告警meta问题讨论&本脑现状了解

### 2022-10-11

 - 一体机246环境ice抛异常分析，最终定位到是dv把日志id的属性改为数值类型导致的ice抛异常，告警没有写入es，并走后续逻辑，已通知dv修改。
 - 一体机合并告警增加字段保存关联告警的所有失陷资产值，用于资产失陷的解除
 - 建行下发soar的告警增加字段support

### 2022-10-12

 - 马上消费客户问题support，慢规则定位，10个正则规则过滤条件优化。优化思路：增加前置过滤条件，对rlike字段先做like短路过滤；优化正则表达式，减少匹配回溯
 - 一体机artifact资产失陷状态未清除bugfix
 - 本脑删除告警合并策略接口response优化

### 2022-10-13
 
 - 一体机发现的对于有些威胁情报，TI返回给本脑的情报信息和直接在威胁情报中心页面展示的内容不一致问题整理
 - 本脑运营规则支持根据打标类型做过滤功能开发

### 2022-10-14
 
 - atom_install ueba相关改动(告警meta，添加属性)合入一体机分支
 - 告警攻击者组受害者组白名单过滤功能
 - 一体机自动化测试问题分析(init_data.sql sql语句异常，导致admin账号没有创建，调用接口登录失败)

### 2022-10-17
 
 - 一体机自动化测试fail case分析
 - 一体机ice规则bugfix，一体机ice规则body直接使用alarmName，而非alarmHql，不用做转换，这是跟本脑不一致的地方
 - 一体机sae、ice和artifact lb-v3.6-dev合入lb-dev分支

### 2022-10-18
 
 - 一体机自动化测试fail case分析
 - 本脑support，ES API接口调用，对应的本脑操作页面及操作步骤整理

### 2022-10-19
 
 - 一体机自动化测试fail case分析
 - 信息安全部sae告警误报问题分析(后面需分析下代码，定位下规则加载两次的原因；讨论下是否需要改下引擎，不支持建同名规则)；安全事件详情页面EDR类合并告警部分字段没有展示，主机IP是前端的问题，其他几个字段是规则没有输出。

### 2022-10-20
 
 - 一体机自动化测试fail case分析
 - 信息安全部sae not occur模板改造告警误报问题分析(看环境数据，很多日志时间是超前8小时的，sae not-occur模板的触发逻辑是以接收到的日志最大时间为标准去判断的。所以会有一些超前时间的告警出来。建议修改下规则，时间窗口改成接收时间。)

### 2022-10-24
 
 - 一体机告警通知相关bugfix
 - 国债项目support，增加合并告警功能(基于本脑2.1版本)

### 2022-10-26
 
 - 国债项目support，合并告警相关build部署及测试
 - 本脑历史任务(定时)未执行问题support，最终定位到是misc没有执行，misc取任务时该任务已过期。

### 2022-10-27
 
 - 国债项目support，合并告警返回值owner字段不是id问题support(hql问题，请求header中transfer_value= false，hql返回值仍翻译了)
 - hash情报匹配合入本脑2.2版本

### 2022-10-28
 
 - 研发一部技术嘉年华准备：SOAR 360BDR应用联动

### 2022-10-31
 
 - 知识云support
 - 国债direction_key

### 2022-11-1
 
 - 浙江电力项目support，增加脆弱性名称黑名单功能，目前资产所有关于脆弱性的查询都做了过滤。存在一个问题是有些脆弱性接口不是资产实现的，页面可能不对应，已知的有artifact
 - 本脑alarm_source字段，合并告警值类型，esper schema类型(告警是int，合并告警是int[]，esper schema应为int[]，否则匹配会抛异常)问题反馈
 - 分析三个模块一体机、本脑dev分支commit差异整理
 - 技术嘉年华BDR support

### 2022-11-3
 
 - 浙江电力项目support，artifact实体画像资产名称支持模糊匹配，ip支持区间匹配
 - 一体机support，搭本脑环境，接入195.4实时数据，后面需用一体机环境连接该环境es，查看安全事件展示效果

### 2022-11-4
 
 - 一体机support，继续搭建本脑环境，195.4 hes-sae-group-0数据因存在内部事件，sip_dip字段es自动给定json mapping格式，导致es写入时因field量过多抛异常。
 - 搭建本脑过程中，发现ice加载规则有问题，已通知本脑相关同事

### 2022-11-7~8
 
 - 继续搭建本脑环境，删除老索引数据，更新es event mapping，对接195.4数据

### 2022-11-9~11
 
 - 本脑内容包环境sae规则改动support
 - ice溯源分析专利整理

### 2022-11-14~18

 - 农行Building Block实现逻辑了解
 - 监管态势代码通读，涉及siem-backend, siem-vis-util

### 2022-11-21~25

 - 新建project，迁移监管态势siem-backend代码

### 2022-11-28

 - 本脑ice工作流程梳理，整理流程图

### 2022-11-29

 - 一体机客户现场问题support，nacos上有两个sae服务，导致部分规则没有被加载

### 2022-11-30

 - 威胁情报回扫专利工作流程梳理

### 2022-12-01~02

 - 本脑artifact工作流程梳理，整理流程图

### 2022-12-05

 - 一体机告警通知功能合入本脑需求了解，目前需求有问题，需另讨论
 - 威胁情报回扫专利编写

### 2022-12-06

 - 建行问题support，部分告警丢失，从消费kafka alarm topic来看，不是sae的问题，sae正常生成告警了，告警也没有延迟，ice没有。无法判断原因，看ice代码把重置id的代码注释了，最终依据告警id查es，看有个id的kafka数据和告警es数据不一致，定位是ice的问题，告警数据被覆盖了。

### 2022-12-07

 - 建行问题support，sae和hql不一致(ipv6问题，及字段不存在!=结果不一致)，部分告警没有生成，但hql查询可以查到
 - 朴朴超市soar应用联动接口联调

### 2022-12-08

 - misc代码走读&代码逻辑整理

### 2022-12-09

 - 本脑3.0告警通知feature开发：#48474 【L3.6代码合入】通知优化

### 2022-12-12

 - 本脑3.0告警通知feature开发，想到合并策略引入的问题(不同规则的告警合并到一起，导致告警通知和soar预案触发有问题)，讨论解决方案

### 2022-12-13

 - 本脑3.0告警通知feature开发
 - 本脑2.2复盘

### 2022-12-14

 - 分级部署模式下规则下发内容说明文档整理
 - IOC情报回扫设计方案评审

### 2022-12-16
 - 本脑v3.0版本通知优化功能整理，通知方式、通知模块、各个模块的通知内容整理。告警使用merge_key做区分
 - 太平洋保险客户现场问题support
 - 资产SIM线上评审。这里可能有个问题，资产量如果百万级，cache怎么弄？

### 2022-12-26
 - 本脑v3.0版本通知优化功能开发，目前，告警、安全事件、报表、系统监控都已修改。

### 2022-12-27
 - 朴朴超市EDR KillProcess接口 soar预案测试

### 2022-12-28
 - 朴朴超市EDR KillProcess接口 soar预案测试support
 - 本脑涉及通知配置的页面&模块整理
 - artifact模块改动：消费日志数据时，不需要判断key是否带discard标记
 - sae模块改动：更新redis获取正则匹配的key列表方法，避免keys命令导致阻塞；威胁情报类告警，sae添加ioc_encode字段，填充ioc密文。

### 2022-12-29
 - 朴朴超市EDR soar预案测试support
 - 数据分权相关代码迁移至tomcat

### 2022-12-30
 - artifacts代码走读
 - 2023计划(本脑后续工作规划，城市安全大脑)


