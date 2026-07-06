标签（空格分隔）： 研发自驱 本脑v5.0版本后

---

### 需求说明

问题描述：
有人下载166万条数据，导致tomcat卡死，我们没有监控，而是投入了很多骨干去攻坚，最后排查出来是系统控制不严谨，如果我们增加一个超过下载阈值的限制，以及告警监控呢？是不是就不会发生这种事情？
优化方案：
增加后端下载阈值限制

### 方案设计

使用注解，在接口函数执行前，先根据请求参数对数据做一次统计，如果超出数量限制，直接返回错误信息，不给用户下载。
注解提供配置：
 - 限制量，max
 - 数量统计相关方法：提供方法的service类，方法名称，方法所需参数

### 涉及接口整理

|页面     |接口     |备注     |
| --- | --- | --- |
|分析中心-智能检索     |POST /discover/get_download_id?limit=xxx(获取downloadId),<br>GET /discover/download/{downloadId}    |excel格式，默认1000，最大10000     |
|分析中心-威胁感知-威胁告警     | 同上    |     |
|分析中心-分析研判-业务系统风险     |POST /asset/businessSystemRisk/export     |excel格式     |
|分析中心-情报管理-自定义情报     |GET /security/ioc-whitelist/export     |excel格式     |
|处置中心-响应处置-封禁IP     |POST /soar/v1/specialAction/export    |excel格式     |
|资漏中心-资产管理-资产列表     |GET /asset/export     |excel格式     |
|资漏中心-资产管理-业务系统管理     |GET /asset/businessSystem/export     |excel格式     |
|资漏中心-资产管理-网段管理     |GET /asset/network/export     |excel格式     |
|资漏中心-漏洞管理     |GET /asset/vul/export     |excel格式     |
|安全大数据-运维监控-监控告警列表     |POST /monitor/alarmLog/exportAlarmLog|excel格式，不勾选的话不能导出，应该没有风险，页面一次性最多100条   |

内容包相关的：属性、事件、实体、安全信息、解析规则、sae规则、ice规则、告警合并规则、告警调整规则、soar相关(自动响应策略、响应预案编排、自动化单元)
监控策略

### Q&A
1. 不同接口限制下载的数量是否不同？暂定不同，允许用户自定义配置
2. 当前能够下载的量，各个service自己去查，注解中提供能够查询的service和对应的方法名及所需参数



