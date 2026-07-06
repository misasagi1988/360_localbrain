# 新版资产SIM

标签（空格分隔）： 360BrainSecurity

---

## 分析模块与资产互动情况整理

 - **sae**
多维度关联分析：资产、脆弱性过滤匹配
配置告警名称、告警内容、告警建议里带${}替换符时，字段值如果是IP并且IP属于某个资产，在其后面补上对应的资产名称
 - **ice**
incident: 资产risk_score会影响安全事件打分
ice-web: api/incident/advice/{id}，告警content/advice中变量值为资产ip，在其后面补上对应的资产名称
 - **artifact**
消费kafka asset的数据，将资产信息同步至内网IP&内网主机实体





