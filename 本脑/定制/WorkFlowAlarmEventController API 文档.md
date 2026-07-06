
## 概述

`WorkFlowAlarmEventController` 是处理事件（安全事件）相关操作的控制器，包括事件的创建、编辑、删除、列表查询、详情查看、反馈、通知下发等。所有接口均以 `/arbiter` 为根路径。

## 通用响应结构

所有接口返回统一的 `ApiResponse` 对象：

```json
{
  "statusCode": 200,
  "data": { ... }, // 实际数据，可能为对象、数组或分页结构
  "messages": null, // 消息提示，可能为字符串或对象
  "auditMsg": ""    // 审计消息
}
```

`statusCode` 为 200 表示成功，其他值表示错误。具体错误码参考 `ApiResponseStatusEnum`。

## 接口列表

|#|方法|路径|描述|
|---|---|---|---|
|1|POST|`/edit/alarm/event/create`|事件创建|
|2|POST|`/edit/alarm/event/create/v2`|事件创建（批量添加，嘉兴总局专用）|
|3|GET|`/read/alarm/event/code/list`|事件添加列表接口|
|4|POST|`/edit/alarm/event/add`|添加进事件接口|
|5|POST|`/read/alarm/event/list`|事件管理列表接口（分页、搜索）|
|6|GET|`/read/alarm/event/detail`|事件详情|
|7|POST|`/edit/alarm/event/delete`|事件管理删除|
|8|POST|`/edit/alarm/event/edit`|事件编辑|
|9|GET|`/read/alarm/event/task/level/type`|获取指挥任务、事件等级、事件类型、研判结果|
|10|GET|`/read/alarm/event/overview`|安全事件概览|
|11|POST|`/edit/alarm/event/notice/send`|通报/通知下发接口|
|12|POST|`/read/alarm/event/template/detail/notice`|模板详情（事件第二步使用展示）|
|13|GET|`/read/alarm/event/detail/feedback/list`|反馈列表（事件中的展示）|
|14|POST|`/read/alarm/event/disposal/list`|处置之后的页面跳转（是否可反馈/可审批）|
|15|POST|`/edit/alarm/event/feedback/confirmation`|反馈确认接口|
|16|POST|`/edit/alarm/event/recall`|通知/通报/预警撤回操作|

---

## 接口详情

### 1. 事件创建

- **路径**: `POST /arbiter/edit/alarm/event/create`
- **描述**: 创建新事件。
- **请求体**: `EventCreateRequest` 对象（JSON）
- **请求参数**:
    - `HttpServletRequest query` (自动注入，包含HTTP请求信息)
- **请求体字段**:
    - `id` (String, 可选): 事件ID（编辑时使用）
    - `associatedTask` (String): 指挥任务
    - `incidentName` (String): 事件名称
    - `incidentType` (String): 事件类型
    - `incidentLevel` (String): 事件级别
    - `incidentDescription` (String): 事件概述
    - `discoveryTime` (Long): 事件发现时间（时间戳）
    - `unitName` (List<String>): 单位名称列表
    - `targetSystemName` (String): 目标系统名称
    - `targetProvince` (String): 目标省份
    - `targetCity` (String): 目标城市
    - `targetDistrict` (String): 目标区县
    - `targetIp` (List<String>): 目标IP地址列表
    - `targetPort` (List<Integer>): 目标端口列表
    - `targetUrl` (List<String>): 目标URL列表
    - `targetDomain` (List<String>): 目标域名列表
    - `sourceAttackerList` (List<SourceAttackerInfo>): 攻击者信息列表
    - `materialsDesc` (String): 事件依据描述
    - `materialsFileUrl` (List<UploadResponse>): 附件信息
    - `analysisResult` (String): 分析结果
    - `alarmVendor` (String): 厂商信息
    - `sourceProduct` (String): 来源产品
    - `handlingSuggestion` (String): 处理建议
    - `alarmId` (String): 告警ID
    - `sourceFrom` (String): 告警来源（incident/alarm_merge）
    - `startTime` (Long): 告警开始时间
    - `alarmName` (String): 告警数据名称
- **响应**: `ApiResponse`，其中 `data` 字段包含创建的事件信息。

### 2. 事件创建（批量添加，嘉兴总局专用）

- **路径**: `POST /arbiter/edit/alarm/event/create/v2`
- **描述**: 为嘉兴总局代码添加事件接口，支持批量添加。因为丽水创建事件接口的告警id只是字符串格式，为了不修改丽水逻辑，额外增加此接口。
- **请求体**: `JiaXingCreateRequest` 对象（JSON）
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **请求体字段**:
    - `code` (String): 代码
    - 其他字段与 `EventCreateRequest` 类似，但额外包含 `sourceInfo` (List<SourceInfo>): 隐患的信息
- **响应**: `ApiResponse`，其中 `data` 字段包含创建的事件信息。

### 3. 事件添加列表接口

- **路径**: `GET /arbiter/read/alarm/event/code/list`
- **描述**: 获取事件添加列表。
- **请求参数**:
    - `sourceFrom` (String, required): 来源（例如 "incident" 或 "alarm_merge"）
    - `namePaths` (List<String>, required): 名称路径列表
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含代码列表。

### 4. 添加进事件接口

- **路径**: `POST /arbiter/edit/alarm/event/add`
- **描述**: 将告警添加到事件中。
- **请求体**: `JiaXingCreateRequest` 对象（JSON）
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含添加结果。

### 5. 事件管理列表接口（分页、搜索）

- **路径**: `POST /arbiter/read/alarm/event/list`
- **描述**: 获取事件管理列表，支持分页和搜索。
- **请求体**: `EventListRequest` 对象（JSON）
- **请求体字段**:
    - `pagination` (AtomPagination): 分页信息（page, size, sort等）
    - `search` (String): 模糊搜索关键词
    - `discoveryStartTime` (Long): 发现时间起始
    - `discoveryEndTime` (Long): 发现时间结束
    - `noticeStatus` (String): 通报状态（已通报：has_notice，未通报：not_notice）
    - `noticeType` (String): 通报类型
    - `incidentType` (String): 事件类型
    - `riskType` (String): 安全隐患类型
- **响应**: `ApiResponse`，其中 `data` 字段包含分页的事件列表。

### 6. 事件详情

- **路径**: `GET /arbiter/read/alarm/event/detail`
- **描述**: 根据ID获取事件详情。
- **请求参数**:
    - `id` (String, required): 事件ID
- **响应**: `ApiResponse`，其中 `data` 字段包含事件详情对象。

### 7. 事件管理删除

- **路径**: `POST /arbiter/edit/alarm/event/delete`
- **描述**: 批量删除事件。
- **请求体**: `EventDeleteRequest` 对象（JSON）
- **请求体字段**:
    - `ids` (String[]): 事件ID数组
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含删除结果。

### 8. 事件编辑

- **路径**: `POST /arbiter/edit/alarm/event/edit`
- **描述**: 编辑事件信息。
- **请求体**: `EventCreateRequest` 对象（JSON）
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **异常**: `JsonProcessingException` 可能抛出
- **响应**: `ApiResponse`，其中 `data` 字段包含编辑后的事件信息。

### 9. 获取指挥任务/事件等级/事件类型/研判结果

- **路径**: `GET /arbiter/read/alarm/event/task/level/type`
- **描述**: 获取指挥任务、事件等级、事件类型、研判结果等选项数据。
- **请求参数**: 无
- **响应**: `ApiResponse`，其中 `data` 字段包含选项数据。

### 10. 安全事件概览

- **路径**: `GET /arbiter/read/alarm/event/overview`
- **描述**: 获取安全事件概览统计信息。
- **请求参数**: 无
- **响应**: `ApiResponse`，其中 `data` 字段包含概览数据。

### 11. 通报/通知下发接口

- **路径**: `POST /arbiter/edit/alarm/event/notice/send`
- **描述**: 下发通报或通知。
- **请求体**: `JSONObject` 对象（JSON），具体字段由前端定义
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含下发结果。如果下发失败，会记录日志并返回 `apiResponse`（可能为null）。

### 12. 模板详情（事件第二步使用展示）

- **路径**: `POST /arbiter/read/alarm/event/template/detail/notice`
- **描述**: 获取模板详情，不同于之前的模板详情，返回自定义格式（用于事件第二步展示）。
- **请求体**: `DetailNoticeRequest` 对象（JSON）
- **请求体字段**:
    - `templateId` (String): 模板ID
    - `orgPathList` (List<String>): 组织路径列表
- **响应**: `ApiResponse`，其中 `data` 字段包含模板详情。

### 13. 反馈列表（事件中的展示）

- **路径**: `GET /arbiter/read/alarm/event/detail/feedback/list`
- **描述**: 获取事件中的反馈列表。
- **请求参数**:
    - `caseId` (String, required): 案例ID
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含反馈列表。

### 14. 处置之后的页面跳转（是否可反馈/可审批）

- **路径**: `POST /arbiter/read/alarm/event/disposal/list`
- **描述**: 处置之后判断页面是否可反馈/可审批。
- **请求体**: `DisposalListRequest` 对象（JSON）
- **请求体字段**:
    - `nodeIds` (List<String>): 节点ID数组
    - `unitId` (String): 组织ID
    - `caseId` (String): 案例ID
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含可反馈/可审批的状态信息。

### 15. 反馈确认接口

- **路径**: `POST /arbiter/edit/alarm/event/feedback/confirmation`
- **描述**: 确认或驳回反馈。前端传值：type -- 确认：Confirm，驳回：Rejection。
- **请求体**: `ConfirmationRequest` 对象（JSON）
- **请求体字段**:
    - `caseId` (String): 案例ID
    - `nodeId` (String): 节点ID
    - `id` (String): 数据ID
    - `type` (String): 类型（Confirm/Rejection）
    - `content` (String): 内容
    - `unitName` (String): 确认单位
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **响应**: `ApiResponse`，其中 `data` 字段包含确认结果。

### 16. 通知/通报/预警撤回操作

- **路径**: `POST /arbiter/edit/alarm/event/recall`
- **描述**: 撤回已下发的通知、通报或预警。
- **请求体**: `RecallRequest` 对象（JSON）
- **请求体字段**:
    - `caseId` (String): 案例ID（撤回的ID）
- **请求参数**:
    - `HttpServletRequest query` (自动注入)
- **异常**: `Exception` 可能抛出
- **响应**: `ApiResponse`，其中 `data` 字段包含撤回结果。

---

## 相关模型类

### EventCreateRequest

参见上述字段列表。

### JiaXingCreateRequest

继承自 `EventCreateRequest` 但包含 `code` 和 `sourceInfo` 字段。

### EventListRequest

包含分页、搜索、时间范围、状态等字段。

### EventDeleteRequest

包含 `ids` 字符串数组。

### DetailNoticeRequest

包含 `templateId` 和 `orgPathList`。

### DisposalListRequest

包含 `nodeIds`, `unitId`, `caseId`。

### ConfirmationRequest

包含 `caseId`, `nodeId`, `id`, `type`, `content`, `unitName`。

### RecallRequest

包含 `caseId`。

### ApiResponse

通用响应对象，包含 `statusCode`, `data`, `messages`, `auditMsg`。

---

## 注意事项

1. 所有 POST 请求的 Content-Type 应为 `application/json`。
2. 部分接口需要 `HttpServletRequest` 参数，由 Spring 自动注入，前端无需显式传递。
3. 时间字段均为时间戳（Long 类型），单位为毫秒。
4. 列表参数如 `namePaths` 在 GET 请求中需使用重复参数名传递，例如 `?namePaths=path1&namePaths=path2`。
5. 错误处理：若发生异常，`statusCode` 非 200，`messages` 可能包含错误信息。