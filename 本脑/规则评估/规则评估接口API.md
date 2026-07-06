# 规则评估接口API-v4.0


## 规则评估API接口

规则最近7天告警量、规则详情通过其他接口拿到，不提供

### 获取规则评估结果列表

```json
POST /analysis/rule-eval/rule/list
request body:
{
	"pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"keyword": "",   //名称模糊检索，选填
	"status": 1,   //是否有效，选填
	"invalidTypes": [1, 2, 3],   //无效原因类型，选填，1数据源不匹配，2字段缺失，3字段值不匹配
	"sorts": [//排序，选填
        {   
		"field": "invalid_type",//无效原因类型
		"order": "desc"
        },
        {   
		"field": "eval_time",//评估时间
		"order": "desc"
        }
    ]
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //规则评估结果列表
		"total": 987,   //评估结果总量
		"list": [{   //评估结果列表
            "ruleId": "HDWJ1RMH0009",   //规则id
			"ruleName": "外网IP短时间内多次远程交互式登录Windows系统失败后成功-疑似Windows账号暴力破解成功",   //规则名称	
			"invalidTypes": [1, 2], //无效原因类型
			"status": 0, //是否有效，1表示是，0表示否
			"evalTime": 1705869006335 //评估时间
		}]
	}
}
```

### 获取单个规则引用事件列表

```json
POST /analysis/rule-eval/rule/event/list
request body:
{
	"ruleId": "33YR12TH0004",   //规则id
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //规则引用事件列表
		"total": 1,   //事件总量
		"list": [{
            "ruleId": "33YR12TH0004",   //id
			"ruleName": "3434",   //规则名称
			"eventName": "全局事件",   //事件名称
			"eventSource": "A",   //事件源
			"eventType": 0   //事件类型，0表示系统事件，1表示内部事件
		}]
	}
}
```

### 获取单个规则引用事件适配数据源列表

```json
POST /analysis/rule-eval/rule/datasource/success/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"ruleId": "0200ILMN0005",   //规则id
	"eventSource": "A",   //事件源
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
		    "xdr": 1,   //1表示xdr，0表示siem
			"dataSourceId": "1cbe65b5-5e7a-4439-8068-98d617f44166",   //数据源id
			"dataSourceName": "poc_IPS",   //数据源名称
			"resolverName": "IPS_天融信_TopIDP_v3.2294_入口规则",   //解析规则
			"resolverChain": "IPS_天融信_TopIDP_v3.2294_入口规则"   //解析规则链
		}]
	}
}
```

### 获取单个规则引用事件未适配数据源列表

```json
POST /analysis/rule-eval/rule/datasource/fail/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"ruleId": "0200ILMN0005",   //规则id
	"eventSource": "A"   //事件源
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //规则引用事件未适配数据源列表
		"total": 1,   //总量
		"list": [{
			"xdr": 1,   //1表示xdr，0表示siem
			"dataSourceId": "1cbe65b5-5e7a-4439-8068-98d617f44166",   //数据源id
			"dataSourceName": "poc_IPS",   //数据源名称
			"resolverName": "IPS_天融信_TopIDP_v3.2294_入口规则",   //解析规则
            "invalidType": 1,   //无效原因类型
            "question": [""]   //未适配原因
		}]
	}
}

```
### 获取单个规则引用事件针对特定数据源的未适配详情

```json
POST /analysis/rule-eval/rule/datasource/fail/detail
request body:
{
	"ruleId": "0200ILMN0005",   //规则id
	"eventSource": "A",   //事件源
    "dataSourceId": "1cbe65b5-5e7a-4439-8068-98d617f44166"   //数据源id
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //未适配详情
		"total": 1,   //总量
		"list": [{
            "invalidType": 1,   //无效原因
            "resolverChain": "",   //解析规则链
            "question": [""]   //未适配原因
		}]
	}
}
```

### 获取单个规则引用内部事件依赖的有效sae规则

```json
POST /analysis/rule-eval/rule/depend/success/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"ruleId": "0200ILMN0005",   //规则id
	"eventSource": "A"   //事件源
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
			"dependRuleId": "HDWJ1RMH0009",   //规则id
			"dependRuleName": "3434"   //规则名称
		}]
	}
}
```

### 获取单个规则引用内部事件依赖的无效sae规则

```json
POST /analysis/rule-eval/rule/depend/fail/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"ruleId": "0200ILMN0005",   //规则id
	"eventSource": "A"   //事件源
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
			"dependRuleId": "HDWJ1RMH0009",   //规则id
			"dependRuleName": "3434",   //规则名称
            "invalidType": 1,   //无效原因类型,1 规则无效，2规则输出字段无效
            "question": ""   //无效原因描述
		}]
	}
}
```

### 获取单个规则忽略数据源数量

```json
POST /analysis/rule-eval/rule/datasource/ignore/count
request body:
{
	"ruleId": "0200ILMN0005"   //规则id
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //规则忽略数据源列表
		"total": 1   //总量
	}
}
```


## 数据源评估API接口

数据源配置详情、适配规则告警量通过其他接口拿到，不提供

### 获取数据源评估结果列表

```json
POST /analysis/rule-eval/datasource/list
request body:
{
	"pageNum": 1,   //页码
	"pageSize": 10,   //数量
	"keyword": "EPP",   //名称模糊检索，选填
	 "sorts": [//排序，选填
        {   
		"field": "valid_count",//适配规则数量
		"order": "desc"
        },
        {   
		"field": "invalid_count",//未适配规则数量
		"order": "desc"
        }
    ]
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],
	"data": {
		"totalCount": 1,   //计数
		"result": [{
			"dataSourceId": "bc393179-02c5-49cd-ad11-71925494fbfa",   //数据源id
			"dataSourceName": "d-EPP",   //数据源名称
			"resolverId": "",   //解析规则id
            "resolverName": "",   //解析规则名称
			"ValidRuleCount": 60,   //适配规则数量
			"InvalidRuleCount": 20,   //未适配规则数量
			"evalTime": 1678097347136   //评估时间
		}]
	}
}
```

### 获取单个数据源适配规则列表

```json
POST /analysis/rule-eval/datasource/sae/success/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
    "dataSourceId": "bc393179-02c5-49cd-ad11-71925494fbfa",   //数据源id
	"ruleName": "EPP"   //规则名称模糊检索，选填
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
			"ruleId": "00JOO8YI0001",   //规则id
			"ruleName": "短时间内大量SSH连接-疑似SSH暴力破解"   //规则名称
		}]
	}
}
```

### 获取单个数据源未适配规则列表

```json
POST /analysis/rule-eval/datasource/sae/fail/list
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"dataSourceId": "bc393179-02c5-49cd-ad11-71925494fbfa",   //数据源id
	"ruleName": "EPP",   //规则名称模糊检索，选填
    "question": "",   //未适配原因模糊检索，选填
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
			"ruleId": "00JOO8YI0001",   //规则id
			"ruleName": "短时间内大量SSH连接-疑似SSH暴力破解",   //规则名称
            "simName": "登录异常",   //告警类型
            "alarmLevel": "警告",   //告警级别
            "question": [""]   //未适配原因描述
		}]
	}
}
```

### 获取单个数据源未适配原因分类统计结果

```json
POST /analysis/rule-eval/datasource/sae/fail/classify/stat
request body:
{
    "pageNum": 1,   //页码
	"pageSize": 20,   //数量
	"dataSourceId": "bc393179-02c5-49cd-ad11-71925494fbfa",   //数据源id
	"invalidType": 1   //无效原因类型，1数据源不匹配，2字段缺失，3字段值不匹配
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {
		"total": 1,   //总量
		"list": [{
			"question": "",   //未适配原因
			"count": 1   //规则计数
		}]
	}
}
```

### 获取单个数据源忽略规则数量

```json
POST /analysis/rule-eval/datasource/sae/ignore/count
request body:
{
	"dataSourceId": "bc393179-02c5-49cd-ad11-71925494fbfa",   //数据源id
}
response body:
{
	"statusCode": 0,   //状态码，0表示正常
	"messages": [],   //信息
	"data": {   //数据源忽略规则列表
		"total": 1   //总量
	}
}
```


### 数据源适配的规则，近7天触发告警的规则数统计

```json
GET /analysis/rule-eval/datasource/result/stat/{id}
response body:
{
	"statusCode": 0,
	"messages": [],
	"data": {
		"alarmCount": 0
	}
}
```

## 下载评估结果(zip包)

```json
GET /analysis/rule-eval/download
```

## 获取模块运行详情

```json
GET /analysis/v1/module/{id}
response body:
{
	"statusCode": 0,
	"messages": [],
	"data": {
		"id": "NEB6FYXF0000",
		"containerName": "secstudy_rule_evaluation",
		"imageVersion": "1.0.0",
		"imageId": "38e2d6c2f7c3",
		"imageName": "secstudy_rule_evaluation_img",
		"moduleName": "规则评估",
		"moduleDesc": "本脑3.0及以上版本规则和数据源评估",
		"threatType": "规则评估",
		"deployTime": "2023-10-16T07:52:02.000+00:00",
		"updateTime": "2023-12-18T09:46:58.000+00:00",
		"imageEnv": "debug=1",
		"hostVolume": "/opt/qihoo/soc/rule_evaluation",
		"bindVolume": "/opt/qihoo/soc",
		"accessMode": "rw",
		"status": "1",
		"containerCpus": 1000000000,
		"containerMemory": 2147483648,
		"hostPort": 0,
		"bindPort": 0
	}
}
```

## 规则评估手动执行

```json
POST /analysis/rule-eval/execute
response body:
{
	"statusCode": 0,
	"messages": []
	}
}
```

## 获取规则评估image运行状态

```json
GET /analysis/rule-eval/status
response body:
{
	"statusCode": 0,   //状态码，0表示正常，1表示正在运行或不存在评估镜像
	"messages": []
	}
}
```