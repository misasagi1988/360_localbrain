# 用户信息

标签（空格分隔）： SELF_INFO

---

**医保局**: 15251852963, Misasagi@1988
**网易邮箱**: meng_yujing@yeah.net, Misasagi@1988
**facebook**: meng_yujing@yeah.net, Misasagi@1988
**obsidian**: meng_yujing@yeah.net, Misasagi@1988
**阿里云**: 15251852963, Misasagi@1988
**github**: misasagi1988, Misasagi880619
**gmail**: mengyujing1988@gmail.com, Misasagi1988
**google 账号**： Inori Misasagi, mengyujing1988@gmail.com
**腾讯云**：meng_yujing@yeah.net, Misasagi@880619
**payroll**：Arcelan0
**teambition**: 主邮箱mengyujing1988@gmail.com, 辅助邮箱meng_yujing@yeah.net
**termius**: 终端工具，apple账号，密码是 Misasagi1988
**360邮箱**: mengyujing@360.cn,  MisasagiQihooS0c, MisasagiArcelan19880506, Q!hooS0cMisasagi, MisasagiArcelan19880506,MisasagiArcelan19881011,MisasagiArcelan880619,ArcelanMisasagi19881011, MisasagiArcelan19880619
**360家**: http://home.qihoo.net/, mengyujing/s43MT^JN$2B^j4^
**360服务器后台密码**：S3cur!tyQ!hooS0c，账号:  mengyujing
**360 gitlab**: mengyujing@360.cn, MisasagiArcelan880619
**hulk**: HanS!gh5#NT_1
**tavily**, 注册账号：meng_yujing@yeah.net, Misasagi@1988
API Key: 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

每天所有的工作内容都要记录在极库云上，项目定开相关的再记录一份在jira上

**s3.qbuild.corp.qihoo.net:8360/nexus**: localbrain/local20201210

**GeoLite2 Free Geolocation Data**: 
https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
https://www.maxmind.com/en/accounts/1031403/people/488d3e54-dbb4-4995-89f8-50bfbe0a558c
meng_yujing@yeah.net/vyk8-XgvBqJt4Q4

 mvn deploy:deploy-file -DpomFile=pom.xml -Dfile=panther-6.2.7.jar -DrepositoryId=localbrain -Durl=[http://s3.qbuild.corp.qihoo.net:8360/nexus/content/repositories/localbrain/](http://s3.qbuild.corp.qihoo.net:8360/nexus/content/repositories/localbrain/)

**github-recovery-codes**

94d9a-050bd
6b07e-f4df9
99660-65ffd
6ade3-9dc16
15299-e9c84
0cfb5-dc5a1
4edd4-e9edd
13859-ebdda
c8904-7cbc0
6ce27-6101e
24ebe-2c59d
5a9cb-1c008
9ed6e-07d7f
cb1cf-4bdd5
6396b-39e48
99821-3728d

党员信息
入党时间2013年5月1号
转正时间2014年5月1号
党员编号：36011045	孟玉静

工作经历
三六零数字安全科技集团有限公司
大数据平台组后端开发工程师   2017.04-至今
工作内容：负责本地安全大脑产品各个版本的实时大数据分析引擎、安全事件自动化溯源分析引擎的设计、开发、难点解决、功能增强、问题修复及日常维护。

趋势科技中国研发中心
CoreTech部门测试工程师   2014.04-2017-04
工作内容：负责SA、SC、0day三个team的自动化测试系统的构建、维护及日常测试。


项目经历
大数据实时流处理智能分析引擎
项目简介：运用流数据分析技术，抽取事件模式，构建关联分析规则引擎，对客户环境中实时产生的海量无界数据进行规则研判，满足触发条件即生成告警，以提醒用户，避免不必要的损失。
项目难点：
1. 支持多类复杂关联分析模式匹配场景，无状态计算、有状态计算；支持告警溯源
2. 同时支持高吞吐量、高性能、低延迟
3. 分布式
4. 高可用
项目技术栈：springboot, kafka, zookeeper, mysql, redis, disruptor
我的职责：
1. 根据既往流处理安全分析的经验，总结整理了一套规则分析模型，依据模板生成不同触发模式的规则，匹配各种流处理安全分析场景，满足安全分析场景的需求
2. 从分析引擎创建、规则创建、实时数据接入、数据处理、告警生成、告警输出等各个工作流程完成整个引擎的设计及开发工作
3. 自定义多种操作符，对各种数据类型的事件字段做过滤匹配
4. 分析引擎性能影响因素，从多种角度对引擎数据处理进行性能优化，保证引擎高性能、低延迟稳定工作
5. 针对不同客户现场实际的数据量，给出多种分布式部署及数据处理方案，并予以实现
6. 各个迭代版本分析引擎功能增强及问题修复


大数据批处理分析引擎
项目简介：以日志为数据源，利用Elasticsearch的过滤聚合能力，以简单易用的搜索语句为入口，通过配置告警触发条件，生成相关规则。弥补流处理无法解决的场景问题，扩充系统威胁信息的监测能力，让用户更容易的参与威胁的检测与发现之中。
项目技术栈：springboot, elasticsearch, kafka, mysql, redis
我的职责：
1. 设计普通聚合分析、同比分析、环比分析、基线分析等多种分析研判模式，满足各种安全分析场景需求
2. 整个引擎的设计及开发工作，主要包括规则创建、定时任务方式执行规则语法、告警研判及输出
3. 各个迭代版本引擎功能增强及问题修复


安全事件自动化溯源分析引擎
项目简介：以原始告警为入口，通过建立安全场景模型，整合全网流量和终端日志、告警、资产及漏洞数据，进行关联分析和行为建模，自动汇聚相关威胁日志、告警及上下文信息，实现攻击源的精准定位、攻击链的全程追踪和攻击痕迹的有效取证，方便安全运维人员分析与处置。
项目难点：
1. 场景模型的构建，关联上下文信息的提取
2. 同时支持高吞吐量、高性能、低延迟
项目技术栈：springboot, kafka, elasticsearch, mysql, redis
我的职责：
1. 针对不同类型的告警，给出不同的溯源分析模型的构建思路，并予以实现
2. 引擎开发，主要包括告警数据接入、处理，安全事件生成及更新、自动化溯源取证、关联上下文信息提取等
3. 前端页面交互
4. 各个迭代版本引擎功能增强及问题修复



360本地安全大脑 2.0 版本
时间：2021年3月 – 2021年9月
软件环境： CentOS、Java
硬件环境(若有)：无
责任描述：开发360本地安全大脑分析引擎部分
项目简介： 360本地安全大脑是基于云计算、大数据、人工智能等新一代信息技术，将360云端安全大脑核心能力本地化部署的一套开放式智能分析、研判、预警、响应、评估的统一安全平台，模块化组合形成多场景方案，可视化、自动化、智能化高效完成态势感知、高级威胁检测、威胁自动化响应、抗攻击能力评估等安全工作。
