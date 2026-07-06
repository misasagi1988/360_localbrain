# UEBA

标签（空格分隔）： 360BrainSecurity

---

## UEBA简介

在UEBA里的概念是 用户(ueba_user_info) , 事件(ueba_anomaly_incident),  告警(ueba_anomaly_alerts)，其中一个用户可以有多个事件，这个事件和本脑的安全事件等价， 然后一个事件可以有多个告警信息，这个单条告警等价与本脑的合并告警。本脑的安全事件对应到UEBA就是一个 ueba_anomaly_incident 的记录，然后一个ueba_anomaly_incident会关联到多个ueab_anomaly_alerts 告警。
一个用户对于一个模型会产生一个事件， 也就是如果有10个恶意模型运行，都命中了这个用户，就会产生10个安全事件。 UEBA这边是重启模型后会删除对应模型之前的告警和事件，但是本脑这里是处置为忽略，并不是物理删除，所以会导致如果多次重启调整，UEAB这边的事件会少于本脑的事件，但是同一时刻，本脑的非忽略的事件和UEBA的安全事件数量是一致的。
人工不处置的情况下，UEBA的所有模型都是实时分析的，肯定是不会被自动处置掉。

恶意用户/资产分析页面，是从单个用户/资产的视角来展示其上发生的恶意行为。恶意行为是在incident索引里的，可疑行为是在alert索引里的。每个用户详情的行为时间轴的卡片，是一个场景的一个alert。

## L3.6版本改动
之前沟通的是这个版本UEBA合并告警不支持任何操作。跟吴昊说了下，处置和确认只是打个标记，他认为UEBA实现不麻烦，可以做。

### UEBA告警写入一体机风险：
- 合并告警列表改造：ICE告警支持查看详情、处置、确认、告警过滤，ueba告警不支持告警过滤。列表项中像攻击者组受害者组等字段没什么内容。
- 合并告警详情页面改造：ice合并告警会展示基础信息，原始告警，历史经验，同类告警，这对ueba告警是不适用的。ueba可以展示用户画像信息和行为时间轴，但有一个问题是行为时间轴只有一个卡片。建议可以加入用户画像信息，同类告警这些。
- 智能查询页面：合并告警列表：ueba告警与本脑字段有很大区别。

### UEBA优化todo list: 
- ice提供接口，create/delete ueba告警。ueba的告警字段需要添加到本脑字段中。
- 安全事件详情页面改造: 安全事件支持处置、SOAR预案，删除操作。需增加发起工单。UEBA安全事件详情展示行为时间轴，操作支持处置和工单。后台接口改造，联动UEBA。
- 合并告警列表改造，表头加告警来源吧？
- 合并告警详情改造
- 恶意用户/资产分析页面改造：移除处置操作，仅支持查看。

attention：
ueba的安全事件处置的话，会通知ice修改处置状态吗？有通知，但是本脑这边之前是把这个状态忽略了的， 上周给宋倚天说了，他那边修改后就可以了。

## 接口
- POST 新增安全事件 
https://127.0.0.1:443/__internal/ice/api/incident/create
请求体示例:
```{"severity":1,"owner":"","incident_desc":"通过浏览器自带工具截屏的提醒","period":86400000,"ueba_alarm":{"incident_setting_id":"9gqhtDIs5hPHcoVx7gB2"},"advice":"无","uba_incident_id":"8898zoIBFDf8_9etoR9j","user_name":"sqe0179","end_time":1660407273000,"priority":26,"title":"截屏提示","type":"UEBA用户安全告警","ict_from":1,"scenario_id":"8898zoIBFDf8_9etoR9j","number":"ueba incident-sqe0179","start_time":1660407123000,"log_type":"anomaly_incidents","modified":"1661321650574","handle_status":1,"department":"tests","entity":"sqe0179","group":"tests"}```

- DELETE 删除安全事件
https://127.0.0.1:443/__internal/ice/api/incident/delete/ts94zoIBFDf8_9et8hd2?startTime=0

- PUT 修改安全事件
https://127.0.0.1:443/__internal/ice/api/incident/update
请求体示例:
```{"severity":1,"owner":"","incident_desc":"通过浏览器自带工具截屏的提醒","period":86400000,"ueba_alarm":{"incident_setting_id":"9gqhtDIs5hPHcoVx7gB2"},"advice":"无","uba_incident_id":"5s98zoIBFDf8_9etlR_X","user_name":"lim0602","end_time":1660407273000,"priority":28,"title":"截屏提示","type":"UEBA用户安全告警","ict_from":1,"scenario_id":"5s98zoIBFDf8_9etlR_X","number":"ueba incident-lim0602","start_time":1659975123000,"log_type":"anomaly_incidents","modified":"1661321650705","handle_status":1,"department":"tests","entity":"lim0602","group":"tests"}```
