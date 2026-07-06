# HQL Language

标签（空格分隔）： 360BrainSecurity

---
## HQL

### function

内置方法参考“painless内置方法.xlsx”
now()
now(String)
ip_in(String, String)
ipToLong(String)
longToIp(String)
_belong(String, Object)
any_match(def, List)
str_like(def, String)
xxx rlike /正则/

### 命令

demo: index == "asset_confirmed_brain50_es7" | where business_id_path=='bsys_XUQC93LE0012' | stats count(id) by risk_level | head 1000

index == "incident_alarm*" | stats limit=100 dc(id) by sae_rule_id |head 1000

- search, 构建过滤表达式，语句起始命令，search可省略，只处理布尔表达式，比较表达式(左侧字段，右侧常量值或字段)，特殊字段index值为索引类型；不支持函数调用
```
grammar: search <logical bool expression>
demo: index == "event" and 事件名称 rlike /.*web.*/ and 源地址 == "127.0.0.1" and status == 404
```

- where, 使⽤Painless表达式筛选搜索结果，Painless表达式必须是布尔值表达式，返回 true 或 false。
```
grammar: where <painless expression>
demo: 
index == "event" | where not ip_in(源地址 , "172.16.0.0/16") and Math.abs(目的端口 - 源端口) > 2; 
index == "event" | where try {return ipToLong(源地址) > ipToLong("1.1.1.1");} catch (Exception e) {return false;}
```

- eval, eval 命令要求指定⼀个字段名，⽤于接受要计算的表达式的结果。
```
grammar: eval <painless expression>
demo: 
# 创建包含计算结果的新字段
index == "event" | eval def _time = 接收时间 - 发生时间; def low = 事件名称.toLowerCase();long _ip = ipToLong(源地址) 
# 创建新的返回对象
index == "event" | eval def map = [:]; map['时间字段']= 发生时间; if (exist 源地址){map.ip=源地址} return map
# 异常捕获
index == "event" | val try {
  def _time = 接收时间 - 发生时间;
  def low = 事件名称.toLowerCase();
  long _ip = ipToLong(源地址);
} catch (Exception e) {
  return doc;
}
```

- bucket, 通过对 field 值桶运算产生新的字段放到该事件中。
```
grammar: bucket [<bucket-options>...]<field> [AS <newfield>]
- 必要参数  
    field  
      语法：<field>  
      描述：指定⼀个字段名称。  
    可选参数  
    bucket-options  
      语法：span | minspan | bins | start-end  
      描述：分桶选项  
    span  
      语法：span = '<time-span>' | '<int-span>'  
      描述：基于时间间隔分桶或者数字间隔分桶  
                <time-span> 为<num><ms|s|m|h|d>格式的字符串，ms-毫秒 s-秒 m-分 h-时 d-天  
                     分桶算法：Math.floor(value / interval) * interval  
                <int-span>为整形数字字符串  
                     分桶算法：Math.floor((value - 0) / interval) * interval + 0  
    minspan | bins  
      语法：minspan = '<time-span>'  bins = <num>  
      描述：基于最小时间间隔和最大分桶数，再根据时间选择器起始结束时间（或者start-end时间戳参数），自动产生最佳时间间隔  
      默认值：bins为15  
    start-end  
      语法：start=<num> | end=<num>  
      描述：将数字型<field>根据大于等于start和小于end的事件产生桶值为start的新字段  
    newfield  
      语法：ID  
      描述：桶字段名  
      默认值：_<field>_bucket  
- ⽤法  
    为每笔事件产生一个分桶字段
- ⽰例  
    ⽰例 1：返回每5分钟跨度内事件总数。
... | bucket span='5m' occur_time  AS _time | stats count(id) BY _time
⽰例 2：最近12小时(时间选择器)，产生最小间隔1分钟切最多50个桶，每个桶里事件总数
... | bucket minspan='1m' bins=50 occur_time | stats count(id) BY _occur_time_bucket
⽰例 3：将源端口根据>=0且<100和>=100且<200产生桶值，其余不符合的事件不会产生桶值
... | bucket start=0 end=100 源端口 AS _range  | bucket start=100 end=200 源端口 AS _range | ...
```

- stats, 计算结果集的聚合统计，如平均数、计数和总和。类似于 SQL 聚合。如果 stats 命令在没有 BY ⼦句的情况下使⽤，将只返回⼀⾏，也就是整个进来的结果集的聚合。如果使⽤了 BY 字段，将为 BY 字段中指定的每个唯⼀值返回⼀⾏(分组字段)。
```
grammar: stats (stats-function(field) [AS field])... [BY field-list]
demo: index == "event"  | stats count(src_address) AS cnt , dc(dst_address) AS dct
```

| 聚合函数        | 功能   |
| ---------- | ------ |
|avg(X) | 返回字段 X 中的值的平均值。   聚合函数|
|count(X)   | 返回包含任意值(非空)的您指定的字段的出现次数。例如:count(id)。 聚合函数|
|dc(X)  | 返回字段 X 中非重复值的计数，目前也已estdc方案实现。    聚合函数|
|estdc(X)   | 返回字段 X 中非重复值的估计计数。    聚合函数|
|max(X) | 返回字段 X 的最大值。  聚合函数|
|min(X) | 返回字段 X 的最小值。  聚合函数|
|range(X)   | 返回字段 X 的最大值与最小值之差(前提是 X 的值为数字)。   聚合函数|
|sum(X) | 返回字段 X 的值的总和。 聚合函数|
|values(X) | 返回字段 X 的去重列表。 聚合函数, 默认10个，limit 配置数量|

- sort, 按指定字段对结果集进行排序，-表示降序，+表示升序
```
grammar: sort <sort by clause>
demo: index == "event" | sort - 目的地址
默认值：升序
```

- fields, 在搜索结果中保留或移除字段
```
grammar: fields +/- <field-list>
demo: index == "event" | sort 目的地址 | fields - src_port , dst_port # 移除源端口、目的端口字段
```

- head, 按搜索顺序返回前 N 个指定结果
```
grammar: head <num>
demo: index == "event" | head 3
```

- top，显⽰字段最常⻅的值。若包含可选的 by-clause，该命令将查找 groupby字段值分组最常⽤的值。
```
grammar: top [<N>] [<top-options>...]<field-list> [<by-clause>]
demo: index == "event"  | top 3 src_address BY event_name
```

- append, 将⼦搜索结果附加到左侧查询结果
```
grammar: append <subsearch>
demo: index == "event"  | stats count(event_name) | append [index == "event" | stats dc(src_address)]
```

- join, 多表联合查询
```
demo: index == 'event' | join max=1 left=l right=r where l.目的地址=r.ip_address [index == 'asset*' ]
index == 'artifact_entity_intranet_ip' and asset_name !== '' and asset_name !== null  |  localop  |  eval   asset_ip=rfc5952Ipv6(intranet_ip) | join max=1 left=L right=R where L.asset_ip=R.intranet [search  index == 'incident_merge_brain45_es7' and intranet belong 内网IP and any_match(incident_type,['alarm_merge']) | stats  limit=1000 count(id) AS  count BY intranet] | sort -risk_level,-asset_importance,-count | head 20
```

- xyseries, 将结果集数据转换为聚合表格形式。供使用者易于理解
```
grammar: xyseries [ xyseries-options ] <x-field> <y-name-field> <y-data-fieldList>
- 必要参数
- <x-field>
  语法：<field>
  描述：用作x轴的字段，该字段会在结果数据表中的第一列。
- <y-name-field>
  语法：<field>
  描述：用作数据系列标签的值的字段，该字段会在结果数据表中的第一行。
- <y-data-fieldList>
  语法：<field> | <field>, <field>
  描述：用作y轴数据的字段，该字段的值会在结果数据表中的数据区域。
demo: index == 'alarm_merge' | bucket span='1d' 开始时间 AS _time | stats sum(alarm_count) AS _sum, count(alarm_level) as _count BY _time,  data_source | xyseries _time data_source _sum, _count
```

- 子查询
子查询执行的结果将作为外部hqlite的参数，常用于如下两个场景：
使用子查询的结果作为主查询的搜索过滤条件；
执行一个独立的搜索，将子查询的结果append或者join到主查询的结果中。
子查询被包含在双方括号[ ]
```
index == 'event' and [index == "alarm" | fields event_id | head 10 | eval id = event_id | fields id| format]
index == "alarm_merge" | where victim_array.ip == "10.16.16.91" | where not exist entrusted_organization and  not (attacker_array.ip belong 内网IP) and any_match(attacker_type, ['IP', '域名']) and victim_type == 'IP'  and attacker_array !== null and attack_direction !== 0  and any_match(incident_type,['alarm_merge']) and [index == "asset_confirmed_brain50_es7" | fields ip_address | eval attacker_array.ip=ip_address | fields attacker_array.ip | format]  | head 10
```
## ES DSL
Elasticsearch Query Language(DSL, domain-specific language)
Elasticsearch 提供了一个可以执行查询的 Json 风格的 DSL（domain-specific language 领域特定语言）。
link: https://www.elastic.co/guide/en/elasticsearch/reference/7.4/query-dsl.html
中文文档: https://doc.codingdict.com/elasticsearch/
### es 字段类型
 - 字符串: keyword, text
 - 数字: long, integer, short, byte, double, float,half_float,scaled_float
 - 日期: date
 - 布尔类型: boolean
 - 二进制类型: binary
 - 数组类型: array，数组不支持混合的数据类型，[]被视为不存在的字段-无值的字段。
 - JSON对象: object
 - JSON对象数组: nested
 - 地理坐标: geo_point
 - IP类型: ip，可以为ipv4和ipv6

### es 查询关键字
| DSL关键字       | 语法含义   |
| ---------- | ------ |
| query|  指定查询条件，json| 
| sort|  指定查询及返回结果排序方式，数组，多个字段，asc/desc| 
| from|  指定返回文档开始的编号，整数| 
| size|  指定返回结果大小，整数| 
| _source|  指定返回结果包含的字段，数组| 
| aggs|  指定聚合逻辑，json| 

### es bool查询分类
| 关键字        | 功能   |
| ---------- | ------ |
|must	|子句（查询）必须出现在匹配的文档中，并将有助于得分。|
|filter	|子句（查询）必须出现在匹配的文档中。 然而不像 must 此查询的分数将被忽略。|
|should	|子句（查询）应出现在匹配文档中。 在布尔查询中不包含 must 或 filter子句，一个或多个should子句必须有相匹配的文件。 匹配 should 条件的最小数目可通过设置minimum_should_match 参数。|
|must_not	|子句（查询）不能出现在匹配的文档中。|

### es聚合函数
| 聚合函数        | 功能   |
| ---------- | ------ |
|avg	| 平均值| 
|value_count	| 指定的字段的出现次数| 
|cardinality	| 字段非重复值的计数| 
|max	| 字段最大值| 
|min	| 字段最小值| 
|sum	| 字段值的总和| 
|extended_stats	| 扩展统计聚合 | 
|missing  |当前文档集上下文中缺少字段值聚合 |
|range	| 字段最大值与最小值之差| 
|ip_range	| IP类型字段专用的范围聚合 | 
|date_range	| 日期类型字段专用的范围聚合 | 
|histogram	| 直方图聚合 | 
|date_histogram	| 日期直方图聚合 | 

## Painless
### Painless简介
Painless支持所有的Java的数据类型及Java API子集。Painless Script具备以下特性：
 - 高性能、安全
 - 支持显式类型或者动态定义类型
Painless可以对es文档进行加工处理，search/update等。
Painless参数：
lang: 指定脚本语言，默认"painless"
source, id: 指定脚本的来源，inline脚本是指定source，存储的脚本是指定的id，并从群集状态中检索。
params: 指定作为变量传递到脚本的任何命名参数。
link: https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-lang-spec.html, https://www.cnblogs.com/sh-jast/p/14944438.html

### demo
```
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": {
            "source": "doc.src_port.size()!=0 && doc.src_port.value==80"
          }
        }
      }
    }
  }
}
```

```
{
"lang": "painless",
"source": "doc['my_field'] * multiplier",
  "params": {
    "multiplier": 2
  }
}
```

```
POST test/type1/1/_update   //update doc
{
    "script" : {
        "inline": "ctx._source.counter += params.count",
        "lang": "painless",
        "params" : {
            "count" : 4
        }
    }
}
```

### 通过painless脚本访问字段
| 操作       | 语法   |
| ---------- | ------ |
|Ingestion | ctx.field_name |
|Update | ctx._source.field_name |
|Search&Aggregation | doc["field_name"] |

### 缓存
脚本编译开销较大，es会将脚本编译后缓存在Cache中，inline script和stored script都会被缓存，默认缓存100个脚本。
保留字符：+ - = && || > <！() {} [] ^"〜*?:\/
如果您需要在查询中使用作为运算符的任何字符（而不是运算符），则应使用反斜杠\转义它们。

### reference
![[hql_vs_spl.xlsx]]
![[Splunk-7.1.0-SearchReference_zh-CN.pdf]]
 
