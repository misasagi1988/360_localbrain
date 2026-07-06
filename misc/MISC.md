# MISC

标签（空格分隔）： 360BrainSecurity

---

### 工时记录
半天以上的工作量，给项目做定制开发、与前场开会讨论、帮忙排查问题的，在jira上填对应项目的工时，并且把工作内容描述清楚  
[http://jira.qa.qihoo.net/projects/BNIM?selectedItem=is.origo.jira.tempo-plugin:tempo-project-sidebar-timesheet](http://jira.qa.qihoo.net/projects/BNIM?selectedItem=is.origo.jira.tempo-plugin:tempo-project-sidebar-timesheet)
只要是给项目上做的事情，非标品研发相关的工作，都填在极库云的系统里做记录  
[https://geelib.qihoo.net/geelib/project/matterType/5320?subId=3215](https://geelib.qihoo.net/geelib/project/matterType/5320?subId=3215)

### MDR管理平台
远程客户环境: http://ui.mdr.360zqaq.net/dashboard

### 本脑proxy登录
- kafka监控，knowstreaming, 认证: admin/Q!hooS0c, https://127.0.0.1/__proxy/kafka-ks
- grafana(prometheus), 认证: admin/Q!hooS0c, https://127.0.0.1/__proxy/grafana

### 更新es mapping
适用与有些脏数据已经导致该索引的es mapping有问题的情况
1. 首先先建立一个新的incident_merge的索引（名称：incident_merge_bak）  
创建索引：curl -X PUT "localhost:9200/incident_merge_bak?pretty"  
2. 同步当前incident_merge_brain21_es7数据到incident_merge_bak（命令执行完毕会一直执行，等待最终返回行说明执行完毕）  
```
curl -XPOST localhost:9200/_reindex -H "content-type: application/json" -d '  
{  
  "source": {  
    "index": "incident_merge_brain21_es7",
    "size":10000  
  },
  "dest": {
    "index": "incident_merge_bak"  
  }
} 
' 
```
 
3. 查看两个索引的docs条数，确认最终一样即可

### DV数据不发kafka情况
数据源配置
事件不存在事件名称
命中全局白名单
存在解析错误：缺少关键字段
发生时间偏移过大，超前10min or 滞后2天

index == "event" | where exist 解析错误 or not exist 事件名称 or 发生时间-接收时间 >600000 | stats count(id)

### DV数据源运行状态
STARTING, PENDING, RUNNING, STOPPING, STOPPED, ERROR
启动中，挂起，运行中，停止中，已停止，错误

### es索引情况
/opt/qihoo/soc/etc/global_config_es_index.properties

### Qradar Env
10.39.170.135
link: https://10.39.170.135/console/qradar/jsp/QRadar.jsp
在南京物理机上装了一个 QRadar，可以用南京有线网访问    admin/Q!hooS0c
后台密码是 root/Q!hooS0c

### hulk 环境
#### 一体机
auto test: 10.217.60.178
3.5 demo环境：10.229.2.55 admin/Q!hooS0c@sw6 mengyujing/Q!hooS0c
3.6 demo环境：10.229.5.78 mengyujing2/Q!hooS0c
4.0 demo环境：11.43.176.66  admin/Q!hooS0c@sw8
10.225.10.246
内置环境一体机后台密码: root/Q!hooS0c@lb

#### 本脑
demo环境：10.202.146.207, dev-ci.localbrain.qihoo.net(10.225.4.161)
v2.2 demo: 10.228.76.241, bndemo22.localbrain.qihoo.net
v3.0 demo: bndemo.localbrain.qihoo.net

#### license
http://10.217.123.123 
360SOC130475901
Zmomo220718!..
里面有签好的license（new）：
http://10.217.123.124/#/login?redirect=%2F
zhaoronglei@360.cn/Q!hooS0c

#### 数据库
oceanbase环境，申请hulk账号：
11.43.181.242
obclient -h127.0.0.1 -P2881 -uroot@sys -p'Q!hooS0c' -Doceanbase -A
达梦数据库：
10.229.1.171:5236 管理员账号密码 SYSDBA/SYSDBA001

#### else
10.36.100.100   root/trend#1..
10.220.188.132   moran/Mmr@2017Wwc@2020
10.202.255.83   admin/Q!hooS0c@sw
10.202.255.83   自己账号：mengyujing/zYm2#lYe7N3h
10.220.188.175
自己hulk环境：myj001v.personal.bjzdt.qihoo.net 10.229.8.156
宋倚天环境：yitian002v.brain.bjzdt.qihoo.net

qa_auto_test环境：qa-auto-test.localbrain.qihoo.net	
 tomcat es dv... 10.208.37.28
 sae ice shuri artifact 10.208.64.16
isc soc准备环境：10.217.105.1 liuyaxiong HanS!gh5#NT1
https://10.218.80.213/ 本脑930 --1.0             admin/Q!hooS0c

一体机L3.5 demo环境： 10.229.2.55  admin/Q!hooS0c@sw6, 在demo环境可以随便访问EPP/EDR、天相、BDR
EPP/EDR: http://10.229.5.138:8081/dist/#/welcome/index, eppadmin/Q!hooS0c
天相: https://10.229.5.68:8080/#/index/dashboard, admin/Q!hooS0c@lb

农行：10.225.8.238 
kafka-producer-network-thread
信息安全部：
wuxuchen W&mb912m87
https://lbrain.sec.qihoo.net/
https://10.16.222.34/03ALX47L0009/global/user/login
https://10.229.4.108/__proxy/es-cerebro
https://10.228.76.241/__proxy/es-cerebro
tomcat: 10.16.222.34
10.229.3.9 sae1
10.229.5.214 sae2
10.229.0.41 ice
10.229.4.108 mysql
10.229.1.189 artifact
10.229.4.108 angler
kafka
10.229.4.108:9092,11.43.177.70:9092,11.43.177.124:9092

### 内容包环境
10.202.255.134   1.0内容包环境
10.228.195.176   1.5内容包环境, dev Q!hooS0c
10.225.7.204   2.0内容包环境, daiqian Q!hooS0c
10.229.5.21   2.1内容包环境, developer developer@123
10.229.5.217  2.1运营环境，admin Q!hooS0c:121
10.202.80.123 3.0内容包环境, sunchuanjie Q!hooS0c
11.33.176.213 3.5内容包环境

内容包密码: HanS!gh5#NT


### 运维环境
10.218.80.217   1.5版本          admin/Q!hooS0c
10.218.80.213   1.0版本          admin/Q!hooS0c
10.218.80.221 企业版6.0GM          admin/S3cur!ty
10.225.1.57   建行定制6.0版本     admin HanS!gh5#NT
建行项目 开发测试环境 内网：https://10.225.1.57/    admin HanS!gh5#NT
https://10.218.80.221/ 企业版6.0GM admin/HanS!gh5#NT

###建行
10.217.62.63
10.217.62.64 
10.217.61.210
用户名密码：xuyufei Xu1yu2fei3__

###国债
10.229.0.71 SOAR
10.229.3.5 SIEM
10.220.188.132 SOC

###Qradar
1344279366@qq.com/mhc360QRadar
songshunan Cyberlab@123

### 各个版本用户名密码
3版本：admin/S3cur!ty
5版本：admin/HanS!gh5#NT
本脑版本：Q!hooS0c
hulk 密码：HanS!gh5#NT_2
es账号：elasticsearch/HanS!gh5#NT

### AD
AD：10.220.188.239   389
登录DN:CN=admin,DC=LocalBrain,DC=cn
DN密码：Abcd@1234
目标DN:OU=Test,DC=LocalBrain,DC=cn
为了区分集团域账号，用户名为姓+名字首字母，密码都是Abcd@1234
如yujinguo，登录名为yujg@LocalBrain.cn，或者LocalBrain\yujg

### 集团git
奇效平台furion：git@w.src.corp.qihoo.net:analysis_engines/furion.git
奇效平台ice：git@w.src.corp.qihoo.net:analysis_engines/ice.git
奇效平台darchrow：git@w.src.corp.qihoo.net:analysis_engines/darchrow.git
集团gitlab地址：w.src.corp.qihoo.net
git@w.src.corp.qihoo.net:foundation/atom-installation.git

### kafka
修改kafka server.properties配置，可以本地往堡垒机发送数据
listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
listeners=INTERNAL://172.16.6.131:9092,EXTERNAL://172.16.6.131:19092
advertised.listeners=INTERNAL://172.16.6.131:9092,EXTERNAL://10.229.3.245:19092
inter.broker.listener.name=INTERNAL

### Qradar doc
https://www.ibm.com/docs/en/SS42VS_7.3.3/com.ibm.qradar.doc/b_qradar_admin_guide.pdf
https://www.ibm.com/docs/en/SS42VS_7.3.2/com.ibm.qradar.doc/b_qradar_users_guide.pdf

### 奇效aws安装
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install -i /usr/local/aws-cli -b /usr/local/bin
/usr/local/bin/aws --version
/usr/local/bin/aws configure

AccessKey ID: IWVS6L4DHMI3F4NY0O8Z
AccessKey Secret: mL7Xi46CPMHLlcrQZhcx5S8s67XwiEjdmQbXm8Bd
endpoint：[http://shanghai.xstore.qihu.com](http://shanghai.xstore.qihu.com)

### 奇效平台版本包获取
查看dev下的包：
/usr/local/bin/aws s3 ls s3://localbrain-build/build/QihooSecBrain/dev/1.5/ --endpoint-url http://pub-shbt.s3.360.cn
/usr/local/bin/aws s3 ls s3://localbrain-build/build/soar/dev/1.5/ --endpoint-url http://pub-shbt.s3.360.cn

1 下载
aws s3 cp s3:s3://localbrain-build/dataviewer/ccb-brain2.2/2.2/dataviewer_ccb-brain2.2_2.2.3356.tar.gz  ./ --endpoint-url http://shanghai.xstore.qihu.com
2 上传
aws s3 cp atom-service/warden/output/warden_lb-dev_L3.5.12261.tar.gz s3://localbrain-build/warden/lb-dev/L3.5/warden_lb-dev_L3.5.12261.tar.gz --endpoint-url http://shanghai.xstore.qihu.com

### 升级项目用的gradle版本
要升级项目使用的 Gradle 版本，您可以按照以下步骤进行操作：
1. **在项目根目录中找到并编辑 `gradle/wrapper/gradle-wrapper.properties` 文件**：
   - 打开该文件，您会看到一个类似于 `distributionUrl` 的属性，指定了当前项目使用的 Gradle 版本。
   - 更新 `distributionUrl` 中的 Gradle 版本号为您想要升级到的版本。例如，将 `distributionUrl` 修改为类似于 `https\://services.gradle.org/distributions/gradle-7.6-all.zip` 这样的链接。

2. **运行 Gradle Wrapper 的 `wrapper` 任务**：
   - 打开命令行工具，进入您的项目根目录。
   - 运行以下命令来执行 Gradle Wrapper 的 `wrapper` 任务，以下载并使用新的 Gradle 版本：
     ```
     ./gradlew wrapper --gradle-version 7.6
     ```
   - 这将更新您的项目中 Gradle Wrapper 的配置，使其使用指定版本的 Gradle。

3. **验证 Gradle 版本**：
   - 运行以下命令来验证 Gradle 版本是否已成功升级：
     ```
     ./gradlew --version
     ```
   - 确保输出显示您所期望的 Gradle 版本号。

通过执行上述步骤，您可以成功将项目中使用的 Gradle 版本升级到 7.6 版本或您所需的任何其他版本。

### docker cmd
```
查看docker镜像: docker ps -a
进入某个名称(secstudy_rule_evaluation)的docker镜像: docker exec -it secstudy_rule_evaluation sh
进入未启动或启动失败的容器：docker run --rm --entrypoint="" -it image:tag bash
执行命令：docker exec -it lbrain-kafka  /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic hes-sae-group-0
```
本脑容器化后调试参考wiki: [容器化后本脑使用指南 | 知识中心 (qihoo.net)](https://geelib.qihoo.net/geelibv3/knowledgeOpen#knowledgeId=1384&docId=150205&anchor=693615666)

要查找哪些镜像正在使用特定镜像，您可以使用以下Docker命令：

**如何用docker命令获取一个镜像被哪些镜像所引用？**
1. 首先，使用以下命令获取特定镜像的ID：
    `docker images`
    从输出中找到要查找引用关系的镜像的ID。
2. 使用以下命令来查找引用了特定镜像的容器：
    `docker ps -a --filter ancestor=<image_id>`
    将`<image_id>`替换为要查找引用关系的镜像的ID。

### gradle cmd
```
./gradlew clean --refresh-dependencies
./gradlew dependencies >d.log
./gradlew dependencyInsight --configuration compile --dependency elasticsearch --warning-mode all
./gradlew clean build
```

### ioc情报查询
```
threat_intelligence_credibility_brain22_es7
{
  "query": {
    "match_all": {}
  },
  "size": 10,
  "stored_fields": [
    "content"
  ]
}
```
### MSS & MDR
MSS: managed security service
该服务通过识别、防护、检测、响应、验证等阶段覆盖整个安全运营全生命周期，通过全视资源管控、全域威胁防御、全知风险检测、全析事件响应、全效结果验证的 “五全安全运营战术”，为客户构建体系化效果导向的安全防护能力。
MDR: managed detection and response
该服务通过全天候专家在线的SaaS化服务、高效精准的平台化运营、全网大数据云地一体化的动态防御等组合服务，实现安全能力的全域打通，为客户提供常态化一站式安全运营保障服务。
安全运营服务主要分为传统的MSS服务（托管式安全服务）和新型的MDR服务（托管式检测与响应服务），前者侧重于管理和维护与安全相关的技术和产品，保障企业IT基础设施稳定运行；后者以更高的视角聚焦攻击与威胁，通过云网端数据共享与分析，提升企业在威胁检测与响应处置方面的能力。

### 搜索告警同比计算逻辑
- es聚合：
无索引，聚合值为空: {}
有索引，无满足条件的查询结果：
{MAX=-Infinity}
{MIN=Infinity}
{AVG=Infinity}
{SUM=0.0}
{COUNT=0}
{DISTINCT=0}
{VARIANCE=0.0}
{STD_DEVIATION=0.0}
- 变化率计算逻辑：
两个都是null/empty：不告警
有一个为null/empty：
old是，cur=infinity/0，不告警，cur正常，max
cur是，old=infinity/0，不告警，old正常，-1
都不是null/empty ：
都是infinity: 不告警
cur=infinity，old=0，不告警，old正常，返回-1
old=infinity，cur=0，不告警，cur正常，返回max
old=0，cur=0，不告警
正常：正常计算

### es agg及query demo:
filter:
```2.2版本es存储优化，请求参数加stored_fields才会展示详细内容
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "ioc": [
              "267C3B325AF52D509F72D582FA228D708885606F391303DA9FA50816AA3F4A2A",
              "B27847689C8B804291C8BCF97862F9E0C1EE5790AF25935212030801551AE633"
            ]
          }
        }
      ]
    }
  },
  "stored_fields": [
    "content"
  ]
}
```
```
{
	"query": {
		"bool": {
			"must": [{
					"term": {
						"id": {
							"value": "679500196295495681"
						}
					}
				}, {
					"regexp": {
						"threat_name": {
							"value": ".*基于443端口的HTTP协议访问.*"
						}
					}
				}

			]
		}
	}
}
```
```
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "src_address": "0.0.0.1"
          }
        }
      ],
      "must_not": [],
      "should": []
    }
  },
  "from": 0,
  "size": 50,
  "sort": [
    {
      "src_address": {
        "order": "asc"
      }
    }
  ],
  "_source": [
    "src_address"
  ]
}
```
```
{
  "query": {
    "bool": {
      "must": [
        {
          "wildcard": {
            "url": "*sae*"
          }
        }
      ],
    }
  },
  "from": 0,
  "size": 10,
  "sort": [
    {
      "create_time": {
        "order": "desc"
      }
    }
  ],
  "aggs": {}
}
```
filter+agg
```
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "sae_rule_id": [
              "7Z55ZQAQ0034",
              "L2PQK8HF0054",
              "324CG45D0511"
            ]
          }
        }
      ]
    }
  },
  "aggs": {
    "alarm": {
      "terms": {
        "field": "sae_rule_id",
        "size": 1000
      },
      "aggs": {
        "cardinality": {
          "value_count": {
            "field": "_index"
          }
        }
      }
    }
  }
}
```

简单聚合
```
{
  "aggs": {
        "event": {
          "terms": {
            "field": "operation",
            "size": 10
          }
        }
      }
}

```
嵌套聚合
```{
  "aggs": {
    "event": {
      "terms": {
        "field": "event_name",
        "size": 1000
      },
      "aggs": {
        "cardinality": {
          "value_count": {
            "field": "src_address"
          }
        }
      }
    }
  }
}
```
二级嵌套聚合
```
{
  "aggs": {
    "alarm_1": {
      "terms": {
        "field": "event_name"
      },
      "aggs": {
        "alarm_2": {
          "terms": {
            "field": "src_address"
          },
          "aggs": {
            "cardinality": {
              "value_count": {
                "field": "_index"
              }
            }
          }
        }
      }
    }
  }
}
```
date_histogram，嵌套聚合
```
{
  "aggs": {
    "timeline": {
      "date_histogram": {
        "field": "occur_time",
        "interval": 3600000,
        "time_zone": "+08:00"
      },
      "aggs": {
        "event": {
          "terms": {
            "field": "event_name",
            "size": 10
          },
          "aggs": {
            "cardinality": {
              "value_count": {
                "field": "src_address"
              }
            }
          }
        }
      }
    }
  }
}
```

### 建行HA demo:
10.217.62.63(主）        
10.217.62.64(备）        
10.217.61.210sae-core集群
xuyufei/Xu1yu2fei3__







