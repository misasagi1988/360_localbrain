shuri_master: 
前端页面交互，威胁情报回扫配置，回收任务增删改查，情报包相关


shuri
威胁情报匹配
情报匹配逻辑：
IpRepuationMatcher: ip match, 本地白名单过滤，黑名单匹配
IpPortMatcher: ip match & ip_port match, 两个都需要本地白名单过滤，黑名单匹配
IpPortUrlMatcher: ip_url match & ip_port_url match，均为本地情报，黑名单
DomainMatcher: FQDN & SLD match, 两个都需要本地白名单过滤，黑名单匹配
DomainPortUrlMatcher: domain_port match & domain_port_url match，均为本地情报，黑名单
UrlMatcher: url match & 引用IpPortMatcher及DomainMatcher


情报回扫: 自动回扫，手动触发，其他模块调用
情报回扫任务页面配置对应数据表: 
```
CREATE TABLE `intelligence_scan` (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` varchar(255)  NOT NULL COMMENT '任务名称',
    `source` varchar(255)  NOT NULL COMMENT '创建来源:手动/自动',
    `type` varchar(255)  NOT NULL COMMENT '自定义/全量回扫',
	`create_time` bigint NOT NULL COMMENT '创建时间',
	`first_schedule_time` bigint  DEFAULT NULL COMMENT '计划调度时间',
	`schedule_time` bigint  DEFAULT NULL COMMENT '调度时间',
	`finish_time` bigint DEFAULT NULL COMMENT '完成时间',
	`status` varchar(255)  DEFAULT NULL COMMENT '任务当前状态',
	`start_time` bigint DEFAULT NULL COMMENT '回扫数据范围',
	`end_time` bigint DEFAULT NULL COMMENT '回扫数据范围',
	`malicious_type` varchar(2550)  DEFAULT NULL COMMENT '情报攻击类型',
	`risk_level` varchar(2550)  DEFAULT NULL,
	`apt_group` varchar(2550)  DEFAULT NULL,
	`run_params` text  COMMENT '运行需要的其他参数',
	`result` VARCHAR(2550)  DEFAULT NULL COMMENT ' 运行完的统计信息',
	 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin COMMENT='回扫运行记录表';
```
Q&A:
source: 具体值: auto/manual
type哪几种，页面有三种，内置360情报包，上传360情报包，上传自定义情报包。代码逻辑: full_scan(全量任务)/custom(自定义内容包任务)
malicious_type 回扫情报类型，映射关系在哪里定义？global_constant_mapping
risk_level回扫情报严重级别，几个值？代码逻辑: critical/high/medium/low
apt_group APT攻击，又有细分子类，通过campaign指定
run_params? 自定义内容包任务使用，内容包导入后指定导入的索引名称indexName
start_time, end_time回扫时间范围: 默认(热数据，7d)，自定义时长N天，以创建时刻为基准设置，代码逻辑: 创建任务时刻为end_time，start_time根据配置推算
status: 几种状态？代码逻辑: ready/running/success/fail
result: 数据格式? json
自动回扫配置：system_config, type = "INTELLIGENCE_FULL_SCAN", 通过cron表达式生成定时任务，写入JOB_DATA，交由misc调度

回扫任务执行：
misc中有定时任务，每5分钟触发一次回扫任务调用，调度入口：http://shuri/intelligence/scan/job/run。回扫任务的运行实际在线程数量为1的线程池里，即回扫任务的并发度是1，每次调度都会判断当前线程池里有没有正在运行的任务，如果没有才会从表里取出可执行的任务进行执行。
回扫任务执行为什么没有用消息通知的机制？如果任务执行过程中重启shuri了呢？
HA模式下多个shuri同时工作时无法决定该任务交由哪个shuri来做，交由misc定时调度可以解决以上两个问题。即使重启shuri，misc仍然会定时调度。
任务运行，执行入口ScanTask.scan
- 加载回扫任务需要的情报信息到内存构建pattern
- 如果是全量回扫任务，如果实时任务的pattern已经加载完成那这里可以直接复用，如果没有加载完成则会重新加载一遍
- 如果是自定义回扫包任务，则会抽取对应索引中情报加载到内pattern中
- 从告警中抽取已经命中过的IOC信息放在内存中用于去重
- 然后开始按照顺序执行匹配：IP_PORT、Domain、Hash、Ipreputation的匹配
- 四种情报匹配逻辑复用的实时情报匹配逻辑


情报回扫问题：
先讲下需求吧，与我自己想的差别太大
自动回扫配置，默认回扫时间范围7d(热数据)，每天定时执行，每天都会有重复的数据被扫描吧？
HA模式？多个shuri呢？


没看懂情报回扫任务执行逻辑：
针对威胁预警特殊处理？
提取告警的ioc，避免重复告警？
扫描数据提取的是artifact的实体数据，提取last_seen_time在[start_time, end_time]范围的实体数据，做ioc情报数据匹配。这里有个疑问，情报回扫可以以定时任务的方式执行，即使不是定时任务，一次性建立多个任务，也要一个一个的依次执行，而任务的start_time, end_time是在创建任务时就定义好了的，一个实体，即使它的last_seen_time不在[start_time, end_time]区间范围，也并不能保证这个实体在这个时间区间范围内没有出现过吧？


ip：ip+port匹配