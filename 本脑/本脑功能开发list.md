# 本脑功能开发List

标签（空格分隔）： 360BrainSecurity

---


## 2026 需求功能列表

- 本脑v5.1版本发布
  - 资产审核功能回归(资产审核检索、发起入库和退库申请、审核入库、变更、退库等资产全生命周期管理)
  - 事件通知通报以及隐患通知通报后端接口代码回归
  - nacos依赖版本
- 本脑v5.1国产化信创适配
  - cpu/os/db 国产化适配(CPU: 海光x86、鲲鹏arm, 操作系统：银河麒麟V10, 数据库：人大金仓V8、 达梦V8、OB)
  - 东方通/宝兰德 tomcat迁移适配
- 智能体平台
  - 智能研判配置功能开发
  - 大屏改造
  - 智能体工作台
- 智能体平台i18n国际化改造

## 2025 需求功能列表

- 本脑v4.5版本优化
   - 多语言支持：attack_insight，XDR旁路分析支持多语言、geo数据表、shuri、tomcat后端及database-mgr数据表、atom-installation多语言支持改造(工作亮点: 部分数据表数据量太大，涉及的改造太多（比如合规相关数据表初始化多语言支持改造），人工改造不现实，研究如何使用kimi大模型自动翻译转换，极大降低改造成本；部分数据表字段长度有限制，翻译为英文后因长度问题导致数据无法正常写入，最终通过更新安装脚本init_data.sh自测更新后的sql文件，成功实现导入；内容包环境i18n改造support；后端隐藏问题(配置文件、代码中文)；、chart、discover_history、属性字段及mapping使用脚本更新；多语言测试bugfix；标品4.5英文版按时发布。
   - 其他

- 本脑v5.0版本开发
   - 资产拓扑功能合入标品
   - 一体机资漏部分优化功能项移植回本脑
   - 资产拓扑功能优化，页面有些变动，功能受license控制
   - 本地情报支持恶意邮件发件箱，shuri变动，sae变动
   - 研发自驱，tomcat连接池达到阈值时告警，f-connection-pool
   - 研发自驱，tomcat中下载数据数量控制，f-connection-pool
   - 研发自驱，威胁图谱详情打开慢问题优化
   - 研发自驱，incident运行监控

- 本脑v5.0国产化信创适配，这个开发耗时将近3个月，尤其是达梦适配，测试将近3个月
  - 东方通中间件适配tomcat: tongweb技术调研，Tomcat应用迁移至TongWeb脚本编写及代码测试，整理Tomcat应用迁移至TongWeb操作手册，tongweb替换tomcat技术分享；
  - cpu/os/db 国产化适配(CPU: 海光x86、鲲鹏arm, 操作系统：银河麒麟V10, 数据库：人大金仓V8、 达梦V8、OB): 主要集中在各种数据库技术调研及安装部署，本脑os适配bugfix。达梦困难最大，出现了很多sql语法不兼容的问题。
  - 东方通+国产数据库，单机部署及HA部署测试support，测试过程中发现了一些本脑一直以来就存在的问题，也有些信创单独的问题。

- 本脑v5.1版本开发
   - ice, 告警调整规则上限
   - 研发自驱，威胁预警页面相关接口优化(相关问题：威胁预警ioc与情报白名单有冲突，怎么办？)

- 定制化
   - 南京银行定制: gpt自动生成告警加白规则，告警加白规则区分来源/并且hql条件支持筛选，ice-web功能适配改造
   - 石化定制问题support：资产拓扑问题定位；规则评估输出定制support；内网IP告警误报问题定位；
   - 宁波银行数据分流后，全局白名单未生效问题support；sae规则不产生告警问题support；
   - 中国移动IT项目资产拓扑接口问题support
   - 城商行SAE数据分流方案制定，sae引擎适配改造；山东城商sae积压严重问题定位，sae rlike优化
   - 邮储银行==redis升级==。邮储redis为带了Kerberos认证的集群部署方式。本脑各个模块jar包、lib中依赖的redis-client依赖jedis-3.8.0.jar升级到4.3.1，因升级到4.3版本后springboot-data-redis依赖失效(2.7.18版本spring依赖的redis为3版本)，导致很多模块启动失败。改动策略是移除springboot的stringRedisTemplate连接redis模式，自己编写jedisCluster集群方法，操作redis。更新了sae、tomcat各个模块、各个组件的相关代码，提供了更新脚本。这个任务耗时很大，接近2周。4.28，客户在现场测试环境测试，发现了不少问题，其中，tomcat、ice-web、sae-monitor是由于缺失部分依赖包导致的，比如json.jar。后面注意，有些间接依赖的包也需要补充，不能单独只换引用包，它本身依赖的其他包也很重要。最保险的策略是直接整个lib包全部替换。
   - ==中石化规则更新时间有误问题==support，石化用的达梦db，mysql的“`update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP”这种ON UPDATE语法不生效。通过咨询gpt，了解了触发器的构造方法，整理了我们所有用到ON UPDATE语法的数据表，写了个批量构造触发器的sql文件，帮他们解决了这个问题。这个问题明显是一个可以避免的问题，在安装环境时就应该做的，而不是等后面客户自己去发现，后面的定位和解决完全是在浪费别人时间。包括后来的合并规则按sae规则名称过滤查询不到，数据库迁移适配问题。
   - ==石化告警加白规则不生效问题==support，分析了三天，最终定位到是规则引用的部分信息组内容为空，ice没有加载，导致的匹配失效，该问题耗费时间较长，也投入很多精力。标品ice存在这个问题。
   - 丽水大数据局，资产运营管理功能开发(6.4~6.20)。基于本脑4.5版本，开发审核模块arbiter，实现该功能，主要包含资产的添加审核、更新审核、删除审核、退库审核、入库审核，审核列表查询、审核执行处理，模块设计时考虑到了支持审核对象类型的多样性。同时，将5.0版本本脑的资产入库退库功能合入该定制分支。
   - 建行检索分析规则告警延迟过高问题support，规则调度时间60min，分析告警数据及规则cron表达式，推理规则定时任务执行时间，定位到是cron表达式的分钟部分有问题，导致创建后任务不能立马执行，而是需要等到第二个小时的对应时间才能执行，导致告警延迟过高。已输出问题分析报告，并优化cron表达式的生成逻辑，确保规则启动后，第一次执行时间距离当前时间不要太长，控制在5min以内。
   - 宁夏银行HA问题support：提供ha问题修复包；给出nginx优化更新文档；解决redis集群搭建失败问题。
   - 中再保险项目支持，提供本脑5.0信创迁移适配方案及迁移支持，tongweb+oceanbase
   
- 安全同事需求
   - 告警类解析规则无对应转换SAE规则的检查工具的开发

- 标品关键bug定位与修复
   - angler 4.5版本，全局白名单转hql语法错误，导致过滤统计结果有问题，无告警，hotfix-4.5、dev都已修复
   - artifact，实体概览问题排查，数据量太大导致es聚合计数统计超时，改为直接从search的total值得到，hotfix-3.5、dev都已修复

## 2024 需求功能列表

- 本脑v4.0版本
   - 规则评估、数据源核心逻辑重构
   - 规则评估后端逻辑改造
   - 内置定制开发框架模块开发
   - tomcat模块kafka producer & consumer生成优化，降低数量
   - kafka关键参数配置统一，统一数据处理流中的kafka producer&consumer重点参数配置，将这些配置放在nacos的base.yml中，每个业务模块引用公共配置来实现。只需要考虑核心数据处理链路。
   - sae&artifact jdk17改造升级
   - 本脑4.0版本HA模式下旁路分析无法正常工作问题bugfix，之前的旁路分析模块在设计时没有考虑HA。HA模式下，tomcat双活运行，每个tomcat机器上都要有相关的镜像，以用来创建容器。目前的策略是镜像上传后放入共享目录，每个tomcat定时任务检查共享目录，有新的镜像包时导入；有镜像删除标记文件时，删除相关镜像；有镜像状态更新标记文件时，更新相关镜像。保证HA模式下镜像文件共享，评估结果共享。但有些情况下只允许一个tomcat操作(比如镜像导入写入db，评估结果写入db)。主要是目前双活tomcat无法互相传送消息。

- 定制化
   - 邮储大数据平台项目support
   - 中石化项目support，hql-plus log增加traceId，协助排查问题
   - 民生银行日审定制化support(定制分支: f-las-custom-2.1-minsheng)，只保留数据查询、数据接入相关页面，其他页面隐藏，数据上报功能定制化，安装部署脚本改造，实现一键部署、内容包导入
   - 新华保险3.0通知策略定制化support：
     - 增加通知策略配置功能，新增全局通知，安全事件等级和威胁告警登记均可发送通知
     - ice添加通知策略匹配逻辑，合并告警及安全事件生成时，满足条件即发送通知
   - 厦门航空项目support， UEBA部分场景用SAE检索分析模块实现，检索分析规则增加两种分析场景，通过配置分析规则，产生类似ueba的分析效果(耗时20+d，新建两种分析算法，分别用来匹配客户提出的两种异常检测场景)
   - 中石化&华能澜沧项目定制：资产拓扑管理、发布及投屏功能开发，后面合入标品
   - 中石化，安全信息多租户改造
   - 宁波银行sae分流support
   
- 本脑v4.5版本
   - 本脑各模块jdk17升级，GC方式改造，统一G1GC
   - tomcat本地配置迁移至nacos
   - 规则评估优化，数据源配置多个解析规则时抛异常处理；plike操作符是否需要做分析？---todo
   - MaxMind GEO db报价问题调研，GeoLite2 ip lib适配，改造ipplus公共组件，同时兼容awdb及geoLite2
   - Kafka topic partition默认数量改造
   - hql正则匹配相关算子(rlike/belong)问题调研与解决思路给定，es支持的正则语法跟java有区别
   - shuri情报匹配接口性能问题分析，给定优化方向(ice端、shuri端的优化思路)
   - misc clickhouse适配改造：dv将数据写入hes-store-group-0，交由transfer模块转储到clickhouse，misc数据过期检测与删除、磁盘空间保护、告警溯源日志备份，数据删除后用能生成告警的日志使用备份数据表数据恢复。

- 安全同事需求
  - 使用pyQt，本脑升级前后规则评估对比分析小工具开发

## 2023 需求功能列表

- 本脑3.0版本
   - 一体机通知合入本脑3.0版本，增加了几种通知方式。多个模块需要做适配改动。
   - 安全事件支持数据分权、责任人分权。为了降低admin用户分配安全事件的压力，支持配置用户查看&分配安全事件的权限，用户开启安全事件运营权限后，可查看并指派归属组织机构下的所有安全事件，包含责任人为自己的、未设置责任人的，责任人为他人的；未开启权限时，用户仅可查询责任人为自己的安全事件。本脑数据分权都是读时分权，走es-proxy实现。这部分只涉及查询，但针对安全事件的一些操作(删除/处置)等是ice自己控制的，这部分ice需要注意修改，做好权限把控。
   - 知识云离线包支持，知识云离线包通过docker镜像的方式提供，安装包中添加该镜像，安装时启动该镜像，在本脑配置了情报云时，如果能访问外网知识云链接，则调用情报云接口，否则调用离线包镜像接口。如果本脑没有启用情报云，则无动作。
   - artifact优化：
       1. 入口页改动：增加接口，输入值(类型选填)即可查询实体详情；增加实体统计信息概览接口。
       2. 实体详情页适配改动，增加该主动访问其他实体数统计、被动访问实体数统计接口、登录账号数统计接口、分布文件数统计接口。
       3. 增加账号实体，对接ueba用户信息，ice安全事件、威胁图谱、实体威胁图谱补充相关信息
       4. 实体关联关系整理及适配改动
   - 数据富化
       1. 更新规则语法，最后一笔日志富化到告警中
       2. ice中提取最后一笔日志数据，获取富化的日志字段，丰富化到告警中
       3. 增加recompile debug接口，改动规则epl，方便系统升级适配
   - 告警名称优化：移除末尾特殊字符
   - 分规则分布式优化：sae增加isolated模式配置，拥有该配置的sae只加载用户手动指定的规则，不参与自动分配规则处理逻辑。引擎可以正常被sae-monitor发现，并在debug页面手动assign规则。

-  一体机v4.0版本需求开发
   - 降本增效
   - 分析相关模块jdk升级至17，springboot升级至3.0.4
   - artifact性能优化: 保证artifact eps的前提下降低artifact的内存占用及磁盘占用，降本增效(通过分析，artifact的内存占用主要来自于: byte[]，geolib导致，通过更新geo可以减少500M+的内存使用；ConcurrentHashMap相关，该变量主要来自于实体及实体关系缓存，实体关系缓存占大多数；rocksdb参数调优)。
   - 本脑3.0功能合入(sae性能优化相关改动合入；告警名称优化--移除末尾特殊字符；【合并告警】后端合入)
   - 告警&安全事件超期自动处置
   - 标品License功能改造适配MSS，为了防止代理商拿MSS的一体机产品和License卖给标品客户，从中赚取差价，我们在产品层面，要做些业务检查，发现并杜绝这种行为。
   - 云脑规则功能开发：本地不再持有360EDR相关规则，sae-monitor定时通过接口获取EDR云脑规则，转换为本地sae规则，允许用户自定义规则标签、通知等内容。

- 本脑3.5版本
   - 一体机告警&安全事件超期自动处置合入本脑3.5版本，并做了优化
   - 通知中心优化
   - 弱口令优化
   - 数据分权，资产相关(未对接资漏，对接资漏)
   - 资漏一体化对接(License整合，资产关联功能)
   - 云脑规则feature开发
   - 容器化开发功能sae sock文件名改动support
   - 情报回扫功能交接
   - 


- 一体机v4.1版本需求开发
   - sae&ice代码改造：鉴于目前lb-dev与dev差别很大，考虑到MSS需求，一体机改为复用本脑代码，在此基础上做JDK升级改造适配，填入一体机独有功能
   - 安全事件处理逻辑优化：本脑安全事件采用周期搜索任务合入告警&日志，为了降低对es的压力，一体机安全事件只在创建时做一次关联告警的向前搜索，后面只根据epl关联合并告警来更新(缺陷：忽略日志，只处理第一层搜索)。
   - artifact改造，数据存储改为ClickHouse，暂时了解了下ck，整理了改造方案wiki


- 本脑v4.0版本
   - 规则评估、数据源评估核心逻辑代码通读，重构 


- 中央国债定制化
   - 增加聚合告警功能
   - 合并策略对象化功能，合并告警输出合并策略名称。
   - 全局白名单优化功能，一个白名单组包含多种类型白名单，与信息组功能不同，无法使用信息组的belong来实现。采用的做法是将关联的白名单配置转变为epl/hql语法添加到过滤条件中，实现数据过滤。
   - sae优化，定位到启动时读取手动assign规则会频繁使用redis keys命令读取redis，导致阻塞，其他模块连接redis timeout，优化sae操作，keys命令使用scan取代，手动assign的规则放入cache。

- 建行定制化
   -  分析引擎下发给soar的告警增加app_code、operation两个字符串字段
   -  xstream依赖包升级至1.4.20
   -  版本升级至本脑2.2，版本升级过程中碰到的问题的support(规则不生成告警，udf返回值)



## 2022 需求功能列表
- dev开发
 - sae-monitor增加配置项，延长FB/OR-FB/RU pattern类规则时间窗口等待时间，合入农行分支。
 - sae-monitor增加debug接口，获取规则引用链，如果事件为内部事件，需进一步溯源至生成该内部事件的规则；sae-core在执行历史任务时，如果规则使用了内部事件，需将生成该内部事件的规则一并加载后执行。合入农行分支。
 - 内部事件逻辑优化，输出到单独topic，dv写入es。sae-core配置文件关于kafka的部分重构。
 - like操作符性能优化。StringUtils方法耗时大，研究并对比几种字符串匹配算法后自行函数实现。参考String.indexOf方法实现。该问题是在信息安全部环境上发现的(A like B, A字符串很长，like性能差)。
 - 分析各个模块，springboot版本升级至2.3.2，gradle版本升级至7.4
 - 搜索告警支持告警静默
 - 双子星模式，规则下发逻辑改造，支持下发至特定节点，条件搜索
 - 本脑XDR安全场景模型ice support
 - 护网support
 - es查询优化，更新scroll为search_after
 - 告警过滤支持inmap/not_inmap操作符
 - 告警输出事件名称组
 - 告警合并策略对象化，数据表更新sql：
 ```
 update sae_rule set alarm_attr=json_set(alarm_attr, '$.mergeStrategy', '4VNXFJ9P0000'), raw=json_set(raw, '$.alert.mergeStrategy', '4VNXFJ9P0000') where JSON_EXTRACT(alarm_attr,'$.enabled') = true and JSON_EXTRACT(alarm_attr,'$.alarmKeyCustomized') = false and sim_name in (select name from attack_scene where scene_type = 'edr');
update sae_rule set alarm_attr=json_set(alarm_attr, '$.mergeStrategy', 'I4TU17CY0000'), raw=json_set(raw, '$.alert.mergeStrategy', 'I4TU17CY0000') where JSON_EXTRACT(alarm_attr,'$.enabled') = true and JSON_EXTRACT(alarm_attr,'$.alarmKeyCustomized') = false and sim_name in (select name from attack_scene where scene_type = 'ndr');
update search_rule set alarm_attr=json_set(alarm_attr, '$.mergeStrategy', '4VNXFJ9P0000'), raw=json_set(raw, '$.alert.mergeStrategy', '4VNXFJ9P0000') where JSON_EXTRACT(alarm_attr,'$.enabled') = true and JSON_EXTRACT(alarm_attr,'$.alarmKeyCustomized') = false and sim_name in (select name from attack_scene where scene_type = 'edr');
update search_rule set alarm_attr=json_set(alarm_attr, '$.mergeStrategy', 'I4TU17CY0000'), raw=json_set(raw, '$.alert.mergeStrategy', 'I4TU17CY0000') where JSON_EXTRACT(alarm_attr,'$.enabled') = true and JSON_EXTRACT(alarm_attr,'$.alarmKeyCustomized') = false and sim_name in (select name from attack_scene where scene_type = 'ndr');
 ```
 - 规则查询增加参数
 - 朴朴超市support，在本脑平台可以一键终止全网所有终端的某个进程，某个终端的某个进程。管控后台为本脑提供针对全网终端终止指定进程、单个终端终止指定进程两个接口，从而实现终止全网终端的某个进程、终止指定终端的某个进程的效果。终止进程按钮界面在本脑实现，下发命令给管控中心后台。
 - 本脑v3.0告警通知功能
 合入一体机3.6版本功能，告警和安全事件支持发送通知，通知方式(邮件/SMS/DINGDING/WEBCHAT/WEBHOOK)。主要涉及sae、ice、misc(负责接收kafka notification消息，发送通知)改动
Q：
  通知对象通过规则来配置。本脑是有合并策略的，也就是不同规则生成的告警可以合并到一起，如果规则的通知配置不一样，那怎么弄呢？通知的内容是告警还是合并告警？通知的模板呢？通知时机，创建&更新？
A：
继续基于sae规则配置soar、通知；基于原始告警触发soar、通知，修改incident实现，预案不再由合并告警触发，转由原始告警触发，incident在触发预案时，复用原合并告警触发接口，并由incident进行数据兼容（新增合并告警的特有字段，如源地址组、目的地址组之类，将原始告警转为合并告警，计数为1），保证旧的预案脚本能够正确执行。
原始告警触发动作的时候使用`规则ID+告警去重策略`进行去重；支持手动配置不基于合并告警策略的去重方式；合入一体机的通知能力，安全事件通知模板套用告警通知。


 

- 农行定制化suppport
 - 历史任务支持更新动态信息组选项配置(sae-core&angler)
 - 更新distinct模板，支持按所属网络区域做分组聚合统计
 - 支持按源地址分组，统计目的地址所属网络区域的个数；支持嵌套ip匹配。所属网络区域仅指本级及直接下级。*后面记得增加debug接口做测试*。
  ```
  demo: 以下面这个tree为例:
  abc-js-branch ("1.1.1.0/24", "1.1.2.0/24")
    abc-js-nj-branch ("2.1.1.0/24", "2.1.2.0/24", "2.1.1.3/24")
    abc-js-sz-branch ("3.1.1.0/24", "3.1.2.0/24", "3.1.1.3/24")
    abc-js-xz-branch ("4.1.30.0/24", "5.1.40.0/24")
  abc-js-branch可以belong所有上面的ip；
  group by "源地址 belong abc-js-branch", 指以上面机构及下属子机构分别为分组做计数；
  group by "目的地址"，count "源地址 belong  abc-js-branch"，指计数源地址匹配该机构及下属子机构的去重数量。
  ```

- 一体机support: 
 - 云端研判优化：sae规则支持silent模式，合入本脑2.5
 - 告警过滤功能，合入本脑2.5
 - XDR模型管理：sae规则细分为SIEM规则及XDR规则；XDR神经元管理；xdr安全事件改造；soar预案联动，合入本脑2.5。
 - XDR安全事件改造
 - 云阵对接：soar应用联动；数据接入及解析规则编写
 - 630 demo环境准备
 - 一体机被动资产发现方案设计&实现
 - 资产优化：被动资产发现；资产解除失陷标记功能
 - 一体机告警通知
 - 分析模块代码整合，合入本脑dev分支代码
 - v3.6版本进度把控，前后端。。。



- 江苏网信办项目: customize-jswx

- 军队项目: f-customize-jdxh
 - 分析各个模块支持国产达梦数据库，合入dev分支

- 其他定制化
 - 浙江电力：分析规则增加用途字段，指明规则用途。
 - 建行：下发soar的告警增加phy_system_cname字段，告警输出为数组，用数组放所有相关日志里的值；6月27日建行SAE积压问题support(优化引擎ip信息组匹配逻辑、优化like匹配逻辑；分析规则，给出规则优化思路)；8.16 分析模块三个分析引擎springboot版本升级至2.7.2，依赖包升级，修复漏洞; 10月10日下发给soar的告警增加send_mail/receive_mail/mail_subject/file_content四个字段，receive_mail/file_content;
 - 邮政储蓄银行poc定制化support：基于2.1 rel拉分支，contain操作符支持左右操作数均为数组，只要两个数组交集非空即可匹配。

## 2021 需求功能列表

### 1.5版本

- sae-not-occur模板功能开发&性能优化：参考https://www.zybuluo.com/mdeditor#1772769
- sae告警response limit功能开发：参考https://www.zybuluo.com/mdeditor#1772787
- sae&ice规则回滚及召回功能开发
- 数据分析模块多语言support
- 分级部署模式下规则下发功能开发：参考https://www.zybuluo.com/mdeditor#1778661
- 分析模块es相关索引可配置，适配es升级改造功能
- sae规则页面添加一个配置项，“静默ICE默认策略”，当这个配置项开启时，告警将不对ICE默认规则生效

### 农行定制

- 搜索告警基线功能：参考https://www.zybuluo.com/mdeditor#1794550
  农行poc support: 检索分析**支持基线功能**，告警输出时附带最近N条基线参考值信息（具体需求：可建立统计分析基线模型（至少支持与设定值比较与历史值偏离度），并产生告警）。合入dev。数据结构定义：
```
@baseline_chart: {
baselineType: sum、count、distinct
baseLineResult: List axisDatas{time, value}  //历史基线值，基线固定每隔一定时间计算一次(与配置的基线窗口有关)，是动态变化的，list size默认值为10
threshold: double，   //根据当前结果与配置的变化率得到阈值，超过阈值则生成告警
currentResult: double，   //当前时间段统计结果
}
@baseline_groupByField: []
@baseline_groupByFieldValue: []
@searchModel: "baseline"   //基线分析模型
@csource: "hql"   //检索分析告警
```

### 2.0版本

- sim 2.0
  sim 2.0改动点：
  sae规则：移除信息模型，改为攻击场景，事件源中，需要选择一到多个实体(必选)
  angler规则：移除信息模型，改为攻击场景，数据配置中增加事件名称和实体配置。
  sae不再区分属性类型，加载所有属性。
- HA，HA采用nacos服务注册发现及配置管理来实现，设计方案：http://wiki.b.qihoo.net/pages/viewpage.action?pageId=13854702
 - angler HA
 - sae-monitor HA
 - sae-core HA由祥瑞来做，目前仅支持分规则部署的HA
- 平台化功能：对本地安全大脑进行平台化改造，将安全分析的基础能力与业务功能进行分离，方便其他产品或模块通过标准的api或者数据流接入本脑。
 - sae主要是提供增删改查highlevel规则及epl规则的接口，及历史任务相关接口。
 - 平台化文档参考：http://wiki.b.qihoo.net/pages/viewpage.action?pageId=13857621
- 【护网反馈需求】SAE规则配置优化
 - 规则里可以配置源地址为受害者组，目的地址为攻击者组
   **实现方案:**
   规则配置页面输出配置中增加一个是否反转攻击角色的勾选框配置，文字描述为 “勾选后源地址为受害者，目的地址为攻击者”，如果勾选了，则将其转成一个标记属性格式，放到输出属性列表中。定义属性名称就叫攻击角色反转，attr_field是attacker_reverse，整形。流式分析及检索分析都支持该功能。
 - 搜索告警增加阈值区间功能
   **实现方案:**
   规则配置页面增加属于/不属于操作符，同比功能本期结果值操作符也增加。字段：lower，表示区间下限；upper，表示区间上限，采用闭区间处理方式。
   之前判断是否触发告警是通过操作符实现Comparable接口来实现的，增加了这两个操作符后，继续用老的方式不合理，换了一种思路，采用guava range，根据操作符配置创建不同的区间范围，调用contains方法校验聚合结果是否在区间范围内及是否要触发告警。
- sae功能增强
 - in操作符功能增强：in操作符除支持ip外，额外添加数组格式字符串支持，元素支持string/ip/整形，demo:
   事件名称 in ["web访问","网络连接"]
   ip in ["1.1.1.1","2.2.2.2"]
   源端口 in [8080,443]
   **实现方案:**
   将字符串转成jsonArray，判断里面的数据元素是否是同一类型，根据类型进一步封装，使用esper自带的in操作符判断。注意字符串元素和整形元素创建epl语句时的区别。
 - 关联分析规则支持dry-run机制，并给出适当的性能预估标准，让用户提前了解该条规则对整体SAE引擎的影响
   **实现方案**
通过分析性能影响因素，暂时给出如下标准，后面看下是否优化：
影响因素1. 操作符
("=")/("!=")/("like")/("rlike")/(">")/(">=")/("<")/("<=")/("exist")/("not_exist")/("in")/("belong")/("contain")/("match");
rlike、belong操作符耗时比较大
影响因素2. 模板
统计类模板(count, count distinct, sum)：时间窗口长度、分组字段数量
关联模板(follow-by)：事件数量、时间窗口长度 
关联模板(repeat-until)：A事件数量、时间窗口长度
关联模板(any-order)：事件数量、时间窗口长度、分组字段数量
关联模板(or-fb,not-fb,not-before)：时间窗口长度
普通模板(not-occur)：时间窗口长度、分组字段数量
fb、ru、or-fb、not-fb、not-before关联条件也有影响
影响因素3. 操作符
rlike: 总分36，4个及以上满分，一个9分
belong: 总分50，5个及以上满分，一个10分
事件数量: 总分4，4个及以上满分，一个1分
分组数量: 总分4，4个及以上满分，一个1分
时间窗口长度: 总分6，1h及以上满分，10min 1分
性能评估标准：
score<10: 优
10≤score<36: 良好
36≤score<50: 一般
50≤score: 较差

### 2.1版本

- HQLite和SAE语法统一：wiki:http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22685172
 - 资产、脆弱性维度关联分析交由sae自己做，增加主机IP维度关联分析
 - 脆弱性数据匹配：脆弱性数据匹配时，需要对每个ip的脆弱性数据做合并，再匹配。为了保证处理性能，目前想到的时数值类放到treeSet里，字符串放到hashSet中，在自定义函数中针对不同操作符做不同处理。<font color="Red">(影响范围: 属性字段都变了，meta更新了，规则要升级)</font>
 - 资产数据匹配：资产维度匹配优化，弃用cast函数，查询资产时对资产数据做转换。
- ipv6 support：单值/区间/前缀
  - sae：in、belong(安全信息/动态信息)操作符，比较类操作符；历史任务滤除全局白名单；多维度(威胁情报、资产、漏洞)测试。注意做性能测试。
  - angler: 过滤条件、统计字段支持ipv6，统计时滤除全局白名单数据
  - ice: belong，内网ip；通知策略；GEO lib信息
  - ice-web：内网ip，资产相关
  - artifact：内网ip
- mysql升级至8版本
- 告警合并策略配置，wiki: http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22684986
 - SIM对象调整：系统内置告警业务实体；修改现有威胁对象，增删必要字段
 - 告警必须包含威胁对象
 - 规则输出配置分两类：威胁字段和附加信息，威胁字段为威胁实体的核心字段；附加信息为其他实体的字段；规则如果输出属性为数组类型，则保存关联日志中该字段出现过的所有值。
 - 增加威胁可信度配置，可引用日志的威胁可信度或使用规则配置的高中低配置；
 - 规则页面允许自定义告警合并字段，也可使用根据攻击场景推荐的合并字段。
 - 告警输出攻击者类型、受害者类型。

    **sae-core, 日志中threat_confidence求max**
    | 模板类型       | epl demo   |
    | ---------- | ------ |
    | normal | 	`threat_confidence` as `threat_confidence` |
    | statistic | 	max(`threat_confidence`) as `threat_confidence` |
    | FB/OR-FB | 	{A.`threat_confidence`, B.`threat_confidence`, ...}.max() as `threat_confidence` |
    | RU | 	{A.max(i -> `threat_confidence`), B.`threat_confidence`}.max() as `threat_confidence` |
    | NBF | 	B.`threat_confidence` as `threat_confidence` |
    | NFB | 	A.`threat_confidence` as `threat_confidence` |
    | any-order,not-occur | 	无法体现在epl中，自己在listener中实现 |
    
    **sae-core, 提取日志中的所有字段值，输出为数组**
    | 模板类型       | epl demo   |
    | ---------- | ------ |
    | normal | 	{`attr_A`} as `attr_B` |
    | statistic | 	window(`attr_A`) as `attr_B` |
    | FB/OR-FB | 	{A.`attr_A`, B.`attr_A`, ...} as `attr_B` |
    | RU | 	A.selectFrom(i->`attr_A`).union({`B.attr_A`}) as `attr_B` |
    | NBF | 	{B.`attr_A`} as `attr_B` |
    | NFB | 	{A.`attr_A`} as `attr_B` |
    | any-order,not-occur | 	无法体现在epl中，自己在listener中实现 |
    
    <font color="Red">**告警输出属性 issue:**</font>
    威胁实体的核心字段无法添加为标记属性
    枚举类型的属性无法配置枚举值
    一个数组的输出属性，是否可以引用多个值
    
    <font color="Red">**告警威胁情报字段输出 issue:**</font>
    统计类规则/关联类规则：告警输出的是最后一个事件的威胁情报字段属性，可能不存在；中间可能有事件有值；如果有多个值的话是否要做合并？
    
    <font color="Red">**升级注意点**</font>
    attack_scene数据表更新。


- sae历史任务使用hqlite1.0
- 搜索告警使用hqlite2.0语法


## 2020 需求功能列表

- 基于百万级EPS的全新SAE分布式的实现
    - 设计思路探索
        - 分级的分布式方案
        - 预聚合事件概念
    - 性能测试探索
     - esper代码优化
    - 方案设计
    - 功能实现
    - 单机性能优化
     - kafka consumer多线程处理
     - esper engine多线程处理
    - debug页面设计与实现
    - 功能测试
    - 性能测试
- 基于SIM模型的多维度关联分析的实现
- 基于Kafka的消息通知的改造
- 全局关联分析功能
- 
## 本脑2.0 dev 合入功能及测试注意点：

- 对redis的操作由redisTemplate改为jedis，注意测一下watchlist、告警静默期功能是否正常。
- 添加了epl逻辑。HA部署时，sae-core无单机模式，duplicate模式下支持加载epl规则，注意检查epl规则功能是否有效，包括接口增删改查及启停操作，sae-core加载情况，assign/removeAssign接口是否正常。



## todo list
 - 本脑2.0内容包，改动alarm_key配置，防止edr场景告警不走默认策略合并
 - 本脑规则配置文档整理
 - ipv6 support
 - 搜索告警优化，不适用misc定时任务触发，自己定时触发。解决搜索告警存在的问题。
    1. searcher_store_room优化，考虑中间结果是否在搜索告警进程内存中保留一份，数据过期是否删除。目前，该部分做了一点优化，每天定期删除子任务在es中的过期数据；全量和同比类型的，目前没有想到好的方式，内存中没必要保存一份，因为中间结果时跟时间窗口相关的，时间是不断变化的。全量的没有将中间结果放入es，同比的也只将部分结果放入es，占用空间不大。
    2. 使用es的聚合来实现，性能较低，如果分片请求过多，影响其他针对es的查询
    2. 分组聚合时，分组数量有限制
    3. 聚合类型支持方差标准差等，不能做子聚合。之前设计存在问题，有分组时，不使能子聚合。当数据已处于冷冻状态时，会影响实际结果
    4. 告警溯源日志id可能会很多，是否需要换一种表达方式
    5. 基线分析，基线结果并不准确
    6. 历史任务有bug：缓存中没有对历史任务和实时任务做分别处理，导致相互影响
    7. 采用cron表达式调用实现，不支持固定延迟多长时间调用一次规则任务。当前cron没有做校验，存在cron不正确导致规则无法调用的情况
    8. 没有做过性能测试
    9. 变化率计算逻辑是否需要改动
 - sae debug页面，duplicate模式下，增加接口，规则被哪个引擎所加载。
 - 资产相关规则语法改动


### sim_model_2版本sae适配
开发工作
 - 规则生成逻辑改动
 - 导入导出改动
 - 页面改动，查询不再支持根据引用事件或生成内部事件名称来查询
 - 内部事件生成逻辑改动
 - 多维度关联分析重构，目前采用map，后面想改为嵌套EventType的形式
升级工作
 - 规则升级
疑问：
 - sim模型场景映射需要重构，之前是放在sae的配置文件中，将对应sim模型映射为相关场景，这种方法存在问题。
 - 内部事件是否需要指定模型？如果使用内部事件的话，只能选用全局模型，不如当前方便
 - 输出属性如何配置？不同场景必须输出字段不同，edr类必须有client_host_sign
 
### sae-core运行时异常, 后面有时间看下，猜测是数据进入引擎后自定义函数对数据有改动
```
(EngineExceptionHandler.java:23) - rule name:zx-having-sum测试（无分组条件） rule epl:[SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, ti_dimension,  WINDOW(id) AS _WINDOW_ID, WINDOW(event_id) AS _WINDOW_IDS, WINDOW(src_address) AS _WINDOW_ENRICH_SIP, WINDOW(src_address_array) AS _WINDOW_ENRICH_SIPS, WINDOW(dst_address) AS _WINDOW_ENRICH_DIP, WINDOW(dst_address_array) AS _WINDOW_ENRICH_DIPS, WINDOW(data_source) AS _WINDOW_ENRICH_DATASOURCE, WINDOW(data_source_array) AS _WINDOW_ENRICH_DATASOURCES, WINDOW(client_host_sign) AS _WINDOW_ENRICH_HOST, WINDOW(client_host_sign_array) AS _WINDOW_ENRICH_HOSTS, WINDOW(attack_id) AS _WINDOW_ENRICH_ATTCK, WINDOW(attack_id_array) AS _WINDOW_ENRICH_ATTCKS FROM GlobalEvent(node_chain_tag is null AND ( spin_tag = 0L AND ( belongs(`src_address`,'R41176V50085')))).win:ext_timed(occur_time,10 sec)  AS A HAVING (sum(A.`src_port`) >= 3306)], event info: 
{"dst_address":"192.168.1.5","dev_address":"172.16.101.169","malware_detection_engine":"kpave","domain_name":"domain1","event_type":"/-1/G1CYSXJW001f/ND2ZURFW005a/W1SPW7AP005c","occur_time":1622449177024,"rule_name_list":["test_zx_new"],"spin_tag":0,"src_address":"172.16.101.160","id":"400150895891841024","vulnerability_id":"CVE-2019-3439","rule_name":"test_zx_new","receive_time":1622449177024,"collector_source":"zx_172.16.101.169","@nbf_state_785":"No A, ActiveTime=1622449169998, EventTime=1622449177024","url":"http://zx.com","data_source":"360EDR","sim_name":"web攻击告警","src_port":3306,"rule_id":"8289fd83-9c18-45af-80b5-65a9ed3372f2","sim_version":"3.1.0000","file_hash":"hash","dst_port":3399,"event_level":0,"event_name":"webshell上传"}
, found an exception:
java.lang.NullPointerException: null

[root@244 logs]# grep "illegal" sae_core.log 
2021-05-31 15:36:34,332:WARN origin-alarm-processor (FurionProcess.java:530) - illegal alarm data: [zx_ice_in_slience] = {dst_address=192.168.1.1, end_time=1622446594320, data_source=360EDR, src_address=172.16.2.246, id=400140063246123008}. err info: missing start_time&end_time or unexpected data types

2021-05-31 16:28:28,885:WARN origin-alarm-processor (FurionProcess.java:530) - illegal alarm data: [普通模板-hyperscan正则全匹配-only-belong] = {dst_address=192.168.1.1, end_time=1622449708872, data_source=360EDR, src_port=3306, domain_name=zx.domain, src_address=172.16.1.246, dst_port=3399, id=400153126624034816}. err info: missing start_time&end_time or unexpected data types

2021-05-31 17:25:00,434:WARN origin-alarm-processor (FurionProcess.java:530) - illegal alarm data: [zx-follow-by测试] = {src_port=3306, start_time=1622453098579, _A={vulnerability_id=CVE-2019-3439 CVE-2009-3439, rule_name=test_zx_new, dst_address=192.168.1.1, receive_time=1622453098579, collector_source=zx_172.16.101.169, dev_address=172.16.101.169, url=http://zx.com, malware_detection_engine=kpave, data_source=360EDR, sim_name=DNS, src_port=3306, rule_id=8289fd83-9c18-45af-80b5-65a9ed3372f2, domain_name=& This is "Domain"1, sim_version=3.1.0000, event_type=/-1/G1CYSXJW001f/I1S4K429005b/7N0U3FS2005e, file_hash=hash, occur_time=1622453098579, rule_name_list=[test_zx_new], spin_tag=0, src_address=172.16.1.246, dst_port=3399, event_level=0, event_name=DNS查询, id=400167344085663744}, _B={dst_address=192.168.1.1, dev_address=172.16.101.169, malware_detection_engine=kpave, domain_name=zx.domain, event_type=/-1/G1CYSXJW001f/ND2ZURFW005a/W1SPW7AP005c, occur_time=1622453100399, rule_name_list=[test_zx_new], spin_tag=0, src_address=172.16.2.246, id=400167351719297024, vulnerability_id=CVE-2019-3439, rule_name=test_zx_new, receive_time=1622453100399, collector_source=zx_172.16.101.169, @nbf_state_785=No A, ActiveTime=1622452606019, EventTime=1622453100399, url=http://zx.com, data_source=360EDR, sim_name=web攻击告警, src_port=3306, rule_id=8289fd83-9c18-45af-80b5-65a9ed3372f2, sim_version=3.1.0000, file_hash=hash, dst_port=3399, event_level=0, event_name=webshell上传}, src_address=172.16.1.246, dst_address=192.168.1.1, dst_port=3399}. err info: missing start_time&end_time or unexpected data types

2021-05-31 17:28:21,413:WARN origin-alarm-processor (FurionProcess.java:530) - illegal alarm data: [zx_ice_out_slience] = {dst_address=192.168.1.1, dev_address=172.16.101.169, data_source=360EDR, start_time=1622453301400, id=400168194778595328}. err info: missing start_time&end_time or unexpected data types

```

### 测试case注意点：
新出一个模板，注意***功能测试***及***性能测试***，性能测试是必须的。




