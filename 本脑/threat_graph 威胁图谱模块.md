关联模块: artifact, ice, attack_insight, web_server
请求情报url: 
threat_graph: https://api.ti.360.net
web_server: https://ti.360.net
提供接口:  /ti/risk, /ti/graph(已废弃)

### 模块功能

消费kafka incident-ioc topic(artifact)的数据，调用大网情报接口，获取相关ip/domain/hash的情报信息，写入threat-graph-ti-result topic，供artifact消费使用。
artifact提取告警可疑ioc，发送到incident-ioc topic，查询大网情报
```//提取语法
SELECT  
  extract_internet_ip(src_address_array, dst_address_array) as internet_ips,  //外网IP(ip)
  domain_name as domain_name,  //域名(domain)
  deduplicate(proc_md5, file_md5) as hash  //hash(hash)
FROM  
  GlobalAlarm(`id` is not null)
```
订阅threat_graph模块提供的threat-graph-ti-result topic的情报更新结果，并动态更新对应实体的威胁等级和是否恶意状态，对应字段：ti_confidence/ti_tags/risk/is_malicious_auto
artifact提供内置接口/artifact/internal/ioc-watchlist，获取当前的黑白名单IOC清单，给ice-web及incident使用，用于对安全事件和合并告警做预研判。

evaluateApi: https://api.ti.360.net/v2/evaluate/, hash情报
smartApi: https://api.ti.360.net/smart/v2, ip/domain情报


### 接口API

```
POST: /threat_graph/ti/risk
request:
{"query_type":"hash","query_list":["0f9824fe751087cd585fddf7825897ee"]} //hash情报
response:
{
	"statusCode": 0,
	"data": {
		"0f9824fe751087cd585fddf7825897ee": {
			"confidence": 20,
			"risk": 40,
			"judge": 10,
			"360": {
				"confidence": 20,
				"risk": 40,
				"judge": 10,
				"key": "0f9824fe751087cd585fddf7825897ee",
				"status": -1,
				"info": [],
				"tags": {
					"source_malicious_type": [],
					"malicious_family": [
						"Mimikatz"
					],
					"other": [
						"Win64/HackTool.Mimikatz.HgEASX0A"
					],
					"malicious_type": [
						"HackTool",
						"木马"
					],
					"file_info": [
						"pe_exe_x64"
					],
					"campaign": []
				}
			},
			"tags": [
				"HackTool",
				"木马",
				"pe_exe_x64",
				"Mimikatz",
				"Win64/HackTool.Mimikatz.HgEASX0A"
			]
		}
	},
	"messages": []
}

```

```
POST: /threat_graph/ti/risk
request:
{"query_type":"domain","query_list":["fget-career.com"]}  //domain情报
response:
{
	"statusCode": 0,
	"data": {
		"fget-career.com": {
			"judgement": {
				"proposal": "此域名为已知的远控指标，请联系安全运营人员确认威胁并采取行动。参考处置建议：第一步：删除广告软件。      第二步：修复被篡改的系统设置，包括注册表、系统服务、计划任务等广告软件常用位置。    ",
				"confidence": "high",
				"targeted": false,
				"risk": "high",
				"type": "远控域名"
			},
			"confidence": "high",
			"base_info": {
				"malicious_family": "Adposhel",
				"malicious_type": "后门软件",
				"campaign": ""
			},
			"evidence_chain": {
				"is_ioc": true,
				"related_url": [],
				"client_ip_counts": -1,
				"cert": {
					"cert_valid": true,
					"SN": "366698012330675772713000885878617357792934"
				},
				"whitelist": 0,
				"is_dyndomain": 0,
				"pdns": [{
					"first_seen": 1695130043,
					"last_seen": 1697576990,
					"confidence": "unknown",
					"rdata": "34.175.230.209",
					"threat_type": [],
					"location": "西班牙 马德里自治区 马德里",
					"risk": "unknown",
					"type": "A"
				}],
				"related_events": [],
				"resolution_counts": -1,
				"whois": {
					"createddate": "2016-06-07 13:50:07",
					"registrant_address": "",
					"registrant_country": "",
					"registrarname": "Dynadot Inc",
					"registrant_email": "",
					"whoisserver": "whois.dynadot.com",
					"nameservers": "ns1.fget-career.com, ns2.fget-career.com, ns3.fget-career.com, ns4.fget-career.com, ns5.fget-career.com, ns6.fget-career.com, ns7.fget-career.com, ns8.fget-career.com",
					"expiresdate": "2024-06-07 13:50:07",
					"registrant_name": "",
					"registrant_organization": "",
					"registrant_telephone": "",
					"updateddate": "2023-05-13 08:56:46",
					"r_domainname": "fget-career.com",
					"status": [
						"clientTransferProhibited"
					]
				},
				"icp": {},
				"feeds": [],
				"pop_rank": 27456,
				"related_sample": [{
						"first_seen": "2023-08-08 19:45:34",
						"file_type": "pe_dll_x86",
						"confidence": "high",
						"reputation": "malicious",
						"threat_type": "感染型病毒",
						"risk": "unknown",
						"family": "Ramnit",
						"md5": "1839cf5ee402750a8b65ff4cbfb91b19"
					},
					{
						"first_seen": "2022-07-25 18:35:21",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "1e2905fc15d3d2f35f8f3b41e4896276"
					},
					{
						"first_seen": "2019-01-10 13:58:33",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "1f65acf4b9ec8648899bf2e951b388f2"
					},
					{
						"first_seen": "2023-07-20 21:43:05",
						"file_type": "pe_exe_x86",
						"confidence": "high",
						"reputation": "malicious",
						"threat_type": "感染型病毒",
						"risk": "unknown",
						"family": "Ramnit",
						"md5": "201d93c5cacd9989f4530063e568dda1"
					},
					{
						"first_seen": "2017-05-08 18:19:46",
						"file_type": "nsis_exe",
						"confidence": "high",
						"reputation": "malicious",
						"threat_type": "感染型病毒",
						"risk": "unknown",
						"family": "",
						"md5": "20e2e0df67eb35855dea79ae499acaaa"
					},
					{
						"first_seen": "2021-09-19 14:17:24",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "2296c39649944ce01ab4022b3eb4e69c"
					},
					{
						"first_seen": "2019-03-04 16:26:14",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "29f0a33990cf428134f09e63ac90746c"
					},
					{
						"first_seen": "2023-07-26 19:30:21",
						"file_type": "pe_dll_x86",
						"confidence": "high",
						"reputation": "malicious",
						"threat_type": "感染型病毒",
						"risk": "unknown",
						"family": "Ramnit",
						"md5": "2ceae24bdd89abc9163b155b6134daaa"
					},
					{
						"first_seen": "2017-04-03 19:00:20",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "bde08d101522a27001a594cb6d7ec31a"
					},
					{
						"first_seen": "2016-10-03 08:42:17",
						"file_type": "pe_exe_x86",
						"confidence": "low",
						"reputation": "unknown",
						"threat_type": "",
						"risk": "unknown",
						"family": "",
						"md5": "c1682c62284733be373e4bc3f5db7df7"
					}
				]
			},
			"risk": "high",
			"judge": "black",
			"tags": [
				"Adposhel",
				"后门软件"
			]
		}
	},
	"messages": []
}
```


artifact 发往incident-ioc topic的数据格式：
```
{
	"from": "",
	"ip_list": [],
	"domain_list": [],
	"hash_list": []
}
```

### 模块联动

1. artifact关注字段，threat-graph-ti-result topic数据格式
```
{
	"ioc": "",
	"ioc_type": "",
	"ti_result": {//ti情报接口返回数据内容
		"detail": {
			"risk": "", //风险等级，ip&domain值: low/medium/high/critical/safe/whitelist/unknown, hash值: 0/10/20/30/40/50
			"confidence": "", //置信度, ip&domain值: low/medium/high/unknown, hash值: 0/10/20/40
			"judge": "", //研判结果，根据风险等级计算得到，ip&domain值: white/black/unknown, hash值: 0/10/20/30
			"tags": [], //标签信息
			"base_info": {//ip会有
				"geo_info": {
					"country": "", //国家
					"province": "", //省份/州
					"city": "" //城市
				}
			}
		}
	}
}
```

2. attack_insight关注的/threat_graph/ti/risk接口返回的字段
```
base_info.malicious_family //恶意家族
base_info.campaign //攻击团伙
```

3. web_server关注的字段
```
hash:  {
	xxx: {
		360.tags.malicious_type,//恶意类型，数组
		confidence,
		risk,
		judge,
		base_info???
		base_info.geo_info,???
		base_info.geo_info.country,???
		base_info.geo_info.province,???
		base_info.geo_info.city,???
		base_info.geo_info.as,???
		base_info.geo_info.asn,???
	}
}

domain: {
	xxx: {
		base_info
		base_info.malicious_family,//恶意家族
		base_info.campaign,//攻击团伙
        base_info.malicious_type,//恶意类型
		base_info.geo_info,???
		base_info.geo_info.country,???
		base_info.geo_info.province,???
		base_info.geo_info.city,???
		base_info.geo_info.as,???
		base_info.geo_info.asn,???
		tags,
		evidence_chain,//证据链
		evidence_chain.pdns,//解析信息，数值
		evidence_chain.whois.registrant_name,//注册人
		evidence_chain.whois.registrant_organization,//所属组织
		evidence_chain.whois.nameservers,//DNS服务器
		evidence_chain.whois.createddate,//注册时间
		evidence_chain.whois.expiresdate,//过期时间
		risk_type,//没找到
		judgement,
		judgement.type,//判定类型
		judgement.confidence,//置信度
		judgement.proposal,//建议
		risk,	
		confidence,???
	}
}

Ip: {
	xxx: {
		tags,
		base_info,
		base_info.geo_info,
		base_info.geo_info.country,
		base_info.geo_info.province,	
		base_info.geo_info.city,
		base_info.geo_info.operator,//ip注册机构
		base_info.geo_info.as,//as组织名称
		base_info.geo_info.asn,/asn
		base_info.network_type,//网络类型
		base_info.anonymous_type,//匿踪类型
		base_info.block_impact,//阻断影响
		base_info.threat_type,//威胁类型
		judgement,
		judgement.confidence,//置信度
		judgement.block_proposal,//阻断建议
		judgement.risk,//风险等级
		risk_type,
		risk,
		confidence,???
	}	
}
```
