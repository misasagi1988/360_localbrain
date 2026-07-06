# SAE 规则模板及EPL语法demo

标签（空格分隔）： SAE_DOC

---

### esper
esper reference: http://esper.espertech.com/release-6.1.0/esper-reference/html/index.html
esper documentation: http://www.espertech.com/esper/esper-documentation/

### pattern语法
http://esper.espertech.com/release-6.1.0/esper-reference/html_single/index.html#event_patterns

### Pattern operator优先级
There are 4 types of pattern operators:

1. Operators that control pattern sub-expression repetition: every, every-distinct, [num] and until
2. Logical operators: and, or, not
3. Temporal operators that operate on event order: -> (followed-by)
4. Guards are where-conditions that control the lifecycle of subexpressions. Examples are timer:within, timer:withinmax and while-expression. Custom plug-in guards may also be used.

| 优先级        | 操作符   |  描述  |  样例  |
| --------   | -----:  | ----:  |   :----:  |
| 1     | pattern guard | where timer:within and while (expression)   |  MyEvent where timer:within(1 sec)<br> a=MyEvent while (a.price between 1 and 10)
|
| 2        |   unary   |   	every, not, every-distinct   |  every MyEvent timer:interval(5 min) and not MyEvent  |
| 3        |    repeat    |  [num], until  |  [1..3] MyEvent until MyOtherEvent  |
| 4        |    and    |  and  |  every (MyEvent and MyOtherEvent)  |
| 5        |    or    |  or  |  every (MyEvent or MyOtherEvent)  |
| 6        |    followed-by    |  -> |  every (MyEvent -> MyOtherEvent)  |


###interesting rules：
1. 符合某个条件的事情持续发生，没有被打断过
This example looks at temperature sensor events named Sample. The pattern detects when 3 sensor events indicate a temperature of more then 50 degrees **uninterrupted within 90 seconds** of the first event, considering events for the same sensor only.
```
every sample=Sample(temp > 50) ->
( (Sample(sensor=sample.sensor, temp > 50) and not Sample(sensor=sample.sensor, temp <= 50))   
  ->
  (Sample(sensor=sample.sensor, temp > 50) and not Sample(sensor=sample.sensor, temp <= 50))   
 ) where timer:within(90 seconds))
```
2. 某个事件一段时间内没有发生：
To test for absence of an event, use timer:interval together with and not operators. The sample statement reports each 10-second interval during which no A event occurred:
```every (timer:interval(10 sec) and not A)```
3. every优先级理解
```
This pattern fires for all A events that arrive within 5 seconds. After 5 seconds, this pattern stops matching even if more A events arrive:
(every A) where timer:within (5 seconds)
This pattern matches for any 2 errors that happen 10 seconds within each other:
every (StatusEvent(status='ERROR') -> StatusEvent(status='ERROR') where timer:within (10 sec))
```

### 操作符
("=");
("!=");
("like");
("rlike");
(">");
(">=");
("<");
("<=");
("exist");
("not_exist");
("in");
("belong");
("contain");
("match");

### 操作数类型
long, double, string, ip, long[], double[], string[], ip[], 字段，数组字段

### 规则模板：

1. normal：

```
SELECT A.`occur_time` AS `start_time`, A.`occur_time` AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, A.`user_account` AS `user_account`, A.`operation_user` AS `operation_user`, id, event_id, data_source FROM GlobalEvent(`windows_event_id`=4720) AS A
```

2. having count:

```
SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, 'ftp下载' AS `sign`, A.`user_account` AS `user_account`, WINDOW(id) AS _WINDOW_ID ,WINDOW(event_id) AS _WINDOW_IDS ,WINDOW(src_address) AS _WINDOW_ENRICH_SIP ,WINDOW(src_address_array) AS _WINDOW_ENRICH_SIPS ,WINDOW(dst_address) AS _WINDOW_ENRICH_DIP ,WINDOW(dst_address_array) AS _WINDOW_ENRICH_DIPS ,WINDOW(data_source) AS _WINDOW_ENRICH_DATASOURCE ,WINDOW(data_source_array) AS _WINDOW_ENRICH_DATASOURCES FROM GlobalEvent(event_name='ftp下载' AND (`result`="/success")).win:ext_timed(occur_time,10 min) AS A GROUP BY A.`user_account` HAVING count(*) >= 50
```

3. count distinct:

```
SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, A.`domain_name` AS `domain_name`, WINDOW(id) AS _WINDOW_ID ,WINDOW(event_id) AS _WINDOW_IDS ,WINDOW(src_address) AS _WINDOW_ENRICH_SIP ,WINDOW(src_address_array) AS _WINDOW_ENRICH_SIPS ,WINDOW(dst_address) AS _WINDOW_ENRICH_DIP ,WINDOW(dst_address_array) AS _WINDOW_ENRICH_DIPS ,WINDOW(data_source) AS _WINDOW_ENRICH_DATASOURCE ,WINDOW(data_source_array) AS _WINDOW_ENRICH_DATASOURCES FROM GlobalEvent(event_name='web访问' AND ( belongs(`dst_address`,'9MJ8DHKV2d36') and not belongs(`src_address`,'CSWLHT4101a6'))).win:ext_timed(occur_time,1 min) AS A GROUP BY A.`src_address`,A.`dst_address` HAVING count(distinct(A.`request_msg`)) >= 300
```

4. having sum:

```
SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, WINDOW(id) AS _WINDOW_ID ,WINDOW(event_id) AS _WINDOW_IDS ,WINDOW(src_address) AS _WINDOW_ENRICH_SIP ,WINDOW(src_address_array) AS _WINDOW_ENRICH_SIPS ,WINDOW(dst_address) AS _WINDOW_ENRICH_DIP ,WINDOW(dst_address_array) AS _WINDOW_ENRICH_DIPS ,WINDOW(data_source) AS _WINDOW_ENRICH_DATASOURCE ,WINDOW(data_source_array) AS _WINDOW_ENRICH_DATASOURCES FROM GlobalEvent( spin_tag = 0L AND (`event_name`!="P2P流量")).win:ext_timed(occur_time,10 min) AS A GROUP BY A.`src_address` HAVING sum(A.`src_port`) >= 10
```

5. follow-by:

```
SELECT A.`occur_time` AS `start_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, B.`occur_time` AS `end_time`, * FROM PATTERN[EVERY A=GlobalEvent(event_name='ftp登录')->(B=GlobalEvent(event_name='ftp下载' AND (A.`src_address`=A.`src_address`) AND (A.id!=B.id)) WHERE timer:within(20 min)) WHILE (A.occur_time <=B.occur_time AND B.occur_time - A.occur_time <=600000) ]
```

```
SELECT A.`occur_time` AS `start_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, C.`occur_time` AS `end_time`, * FROM PATTERN[EVERY A=GlobalEvent(event_name='ftp登录')->B=GlobalEvent(event_name='ftp下载' AND (A.id!=B.id)) WHERE timer:within(20 min)->(C=GlobalEvent(event_name='ftp上传' AND (A.`src_address`=B.`src_address` and B.`src_address`=C.`src_address`) AND (A.id!=C.id AND B.id!=C.id)) WHERE timer:within(20 min)) WHILE (A.occur_time <=B.occur_time AND B.occur_time <=C.occur_time AND C.occur_time - A.occur_time <=600000) ]
```

6. or-follow-by:

```
SELECT A.`occur_time` AS `start_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, B.`occur_time` AS `end_time`, * FROM PATTERN[(EVERY A=GlobalEvent(event_name='web访问')->(B=GlobalEvent(event_name='WEB攻击' AND (A.`src_address`=B.`src_address`) AND (A.id!=B.id)) WHERE timer:within(10 min))) OR (EVERY A=GlobalEvent(event_name='WEB攻击')->(B=GlobalEvent(event_name='web访问' AND (A.`src_address`=B.`src_address`) AND (A.id!=B.id)) WHERE timer:within(10 min)))]
```

7. not-follow-by:

```
SELECT min(A.`occur_time`) AS `start_time`, max(A.`occur_time`) AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, A.id as id, A.event_id as event_id, A.data_source as data_source FROM PATTERN[EVERY A=GlobalEvent(event_name='web访问') -> (timer:interval(10 sec) AND NOT B=GlobalEvent(event_name='ssh登录'))]
```

8. repeat-until:

```
SELECT A[0].`occur_time` AS `start_time`, A[0].`net_protocol` AS `net_protocol`, A[0].`src_address` AS `src_address`, A[0].`src_port` AS `src_port`, A[0].`dst_address` AS `dst_address`, A[0].`dst_port` AS `dst_port`, A[0].`vulnerability_id` AS `vulnerability_id`, B.`occur_time` AS `end_time`, * FROM PATTERN[EVERY [3] A=GlobalEvent(node_chain_tag is null AND (event_name='web访问'))->(B=GlobalEvent(node_chain_tag is null AND (event_name='web攻击上传下载') AND (A[0].`src_address`=B.`src_address`)) WHERE timer:within(20 min)) WHILE (A[0].occur_time <=B.occur_time AND B.occur_time - A[0].occur_time <=600000) ]
```

9. not-before

```
SELECT B.`occur_time` AS `start_time`, B.`src_address` AS `src_address`, B.`occur_time` AS `end_time`, B.id as id, B.event_id as event_id, B.data_source as data_source FROM PATTERN[EVERY (A=GlobalEvent(setActiveTime('25', A, 'occur_time') AND updateNbfState((event_name='web访问'), '25', A, 'occur_time', 'src_address','dst_address')) OR B=GlobalEvent(isNotBefore((event_name='WEB攻击'), '25', B, 'occur_time', 600000, 'src_address','dst_address')))] 
```
//25表示规则id，'src_address','dst_address'为关联条件引用字段

进一步优化：该优化将@nbf_state放入event中，会因改动数据导致并发异常，就移除了getNbfState逻辑
```
SELECT min(B.`occur_time`) AS `start_time`, max(B.`occur_time`) AS `end_time`, B.`src_address` AS `src_address`, B.`src_port` AS `src_port`, B.`dst_address` AS `dst_address`, B.`dst_port` AS `dst_port`, B.id as id, B.data_source as data_source, B.client_host_sign as client_host_sign, B.attack_id as attack_id, B.ti_dimension as ti_dimension, B.event_id as event_id, B.data_source_array as data_source_array, B.client_host_sign_array as client_host_sign_array, B.attack_id_array as attack_id_array, getNbfState(B, 'QB3J7DUA000f') AS `@nbf_state` FROM PATTERN[EVERY (A=GlobalEvent(setActiveTime('QB3J7DUA000f', A, 'occur_time') AND updateNbfState((event_name='ip地址欺骗'), 'QB3J7DUA000f', A, 'occur_time')) OR B=GlobalEvent(isNotBefore((event_name='漏洞扫描' AND (`dst_port`=8088)), 'QB3J7DUA000f', B, 'occur_time', 3000)))]    QB3J7DUA000f为规则id
```

10. any-order

```
SELECT irstream * FROM GlobalEvent(onCase((event_name='webshell上传' AND ( belongs(`src_address`,'V3SD2MBU5b01'))), 'I1HSC04F0011', 0, 2, *, 'src_address') OR onCase((event_name='漏洞扫描' AND ( belongn(`src_port`,'J4VBKV194215'))), 'I1HSC04F0011', 1, 2, *, 'src_address')).win:ext_timed(occur_time, 10 min) HAVING (TRUE)
```
//I1HSC04F0011表示规则id，0/1为事件序号，2为事件总数，'src_address'为分组字段

11. not-occur

```
SELECT null FROM GlobalEvent(isNotOccur('15E1BSP50001', A, 'occur_time', 1000, (event_name='A'), 'src_address')) AS A
```
//15E1BSP50001为规则id，A为事件别名，occur_time及1000为时间窗口配置，(event_name='A')为过滤条件，'src_address'为分组字段，可以不存在或有多个

12. match_recoginze
```
select * from TemperatureSensorEvent
match_recognize (
  partition by device
  measures A.id as a_id, B.id as b_id, A.temp as a_temp, B.temp as b_temp
  pattern (A B)
  define 
    B as Math.abs(B.temp - A.temp) >= 10
)
```
match_recognize对数据顺序要求严格，每个partition的数据要连续，中间有一个不满足，重新算起。适合表达在某个分组条件下，满足条件的数据持续发生，中间没有因不匹配条件而间断的情况，这与follow-by语法有很大不同，follow-by不要求数据必须连续而不间断。

###多维度

1. 威胁情报维度

```
SELECT A.`occur_time` AS `start_time`, A.`occur_time` AS `end_time`, A.`src_address` AS `src_address`, A.`src_port` AS `src_port`, A.`dst_address` AS `dst_address`, A.`dst_port` AS `dst_port`, id, data_source, client_host_sign, attack_id, ti_dimension, event_id, data_source_array, client_host_sign_array, attack_id_array FROM GlobalEvent(node_chain_tag is null AND (event_name='威胁情报IP匹配事件' AND (spin_tag = 2L and cast(ti_dimension('alert'), long)=1 and "C2" in (convertToArray(ti_dimension('tags'))) and cast(ti_dimension('protocol'), string)="UDP"))) AS A
```

2. 2.1版本及以后，脆弱性数据比较特殊，一个IP可对应多条脆弱性数据，需要把所有的数据收集起来，形成一个集合后再去做匹配。匹配逻辑是只要集合中有一个数据满足条件即匹配。具体匹配逻辑参考http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22703207
以操作数为例，举例说明匹配函数：
long, double, string, ip, long[], double[], string[], ip[], 字段，数组字段
severity, double, source, ip_address, port_array, double_array, cve_list, ip_address_array, port, cve_list

exist, not_exist: 
vulContextInvoke(A, 'dst_address', 'ip_address', 'exist', 'exist_check') 
vulContextInvoke(A, 'dst_address', 'double_array', 'not_exist', 'exist_check') 

=, !=: 
vulContextInvoke(A, 'dst_address', 'severity', '=', 3) 
vulContextInvoke(A, 'dst_address', 'severity', '!=', 1)
vulContextInvoke(A, 'dst_address', 'source', '=', 'edr') 
vulContextInvoke(A, 'dst_address', 'source', '!=', 'xdr')
vulContextInvoke(A, 'dst_address', 'port', '=', src_port) 
vulContextInvoke(A, 'dst_address', 'port', '!=', dst_port)
vulContextInvoke(A, 'dst_address', 'source', '=', data_source)

(">");(">=");("<");("<="): 
vulContextInvoke(A, 'dst_address', 'severity', '>=', 1) 
vulContextInvoke(A, 'dst_address', 'severity', '<', 5)

("like"): 
vulContextInvoke(A, 'dst_address', 'source', 'like', 'edr') 
vulContextInvoke(A, 'dst_address', 'cve_list', 'like', 'cve')

("rlike"): 
vulContextInvoke(A, 'dst_address', 'source', 'rlike', 'edr')

("in"): 
vulContextInvoke(A, 'dst_address', 'severity', 'in', {3L,5L})
vulContextInvoke(A, 'dst_address', 'source', 'in', {\"edr\",\"xdr\"}) 
vulContextInvoke(A, 'dst_address', 'ip_address', 'in', \"172.16.0.0/16\") 

("contain"): 
vulContextInvoke(A, 'dst_address', 'port_array', 'contain', 80)
vulContextInvoke(A, 'dst_address', 'cve_list', 'contain', 'CVE-2020-1111')
vulContextInvoke(A, 'dst_address', 'port_array', 'contain', src_port)
filter:
目的地址.脆弱性.IP地址 exist and 目的地址.脆弱性.端口 = 8080 and 目的地址.脆弱性.处置状态 = "待处置" and 目的地址.脆弱性.严重等级 >= "中危" and 目的地址.脆弱性.网址 like "domain" and 目的地址.脆弱性.CVE列表 contain "CVE-2020-0101" and 目的地址.脆弱性.端口 = 目的端口 and 源端口 = 目的地址.脆弱性.端口 and 目的地址.脆弱性.IP地址 in "172.16.0.0/16" and 目的地址.脆弱性.端口 in [80,70,90] and not 目的地址.脆弱性.IP地址 belong 内网IP
epl: 
SELECT A.`occur_time` AS `start_time`, A.`occur_time` AS `end_time`, A.`threat_name` AS `threat_name`, A.`threat_type` AS `threat_type`, A.`event_name` AS `event_name`, A.`event_level` AS `event_level`, `id`, `data_source`, `client_host_sign`, `attack_id`, `ti_dimension`, `event_id`, `data_source_array`, `client_host_sign_array`, `attack_id_array` FROM GlobalEvent(`node_chain_tag` is null AND ( `spin_tag` = 0L AND (vulContextInvoke(A, 'dst_address', 'ip_address', 'exist', 'exist_check') and vulContextInvoke(A, 'dst_address', 'port', '=', 8080) and vulContextInvoke(A, 'dst_address', 'handle_status', '=', 1) and vulContextInvoke(A, 'dst_address', 'severity', '>=', 1) and vulContextInvoke(A, 'dst_address', 'url', 'like', "domain") and vulContextInvoke(A, 'dst_address', 'cve_list', 'contain', "CVE-2020-0101") and vulContextInvoke(A, 'dst_address', 'port', '=', dst_port) and vulContextInvoke(A, 'dst_address', 'port', '=', `src_port`) and vulContextInvoke(A, 'dst_address', 'ip_address', 'in', "172.16.0.0/16") and vulContextInvoke(A, 'dst_address', 'port', 'in', {80L,70L,90L}) and not vulContextInvoke(A, 'dst_address', 'ip_address', 'belong', 'CSWLHT4101a6')))) AS A

###本脑3.0版本规则改动(输出*，适配告警富化)

#### 普通模板

```sql
SELECT src_address, A.* as A  FROM GlobalEvent(event_name = 'A') AS A;   //MapEventBean,MapEventBean
```
<font color='red'>不能直接用select *，与其他字段有冲突，会导致编译错误。</font>
Listener中，select内容是放在一个MapEventBean对象中，A属性是一个MapEventBean类型，可以通过getUnderlying()方法拿到。

#### 统计类模板

```sql
SELECT src_address as src_address, A.* as A FROM GlobalEvent(event_name='A').win:ext_timed(occur_time,10 min) AS A group by src_address HAVING count(*) >= 2;  //MapEventBean,MapEventBean
```
<font color='red'>不能直接用select *，与其他字段有冲突，会导致编译错误。</font>
Listener中，select内容是放在一个MapEventBean对象中，A属性是一个MapEventBean类型，可以通过getUnderlying()方法拿到。

#### 关联类模板: follow-by

```sql
SELECT A.`src_address` AS `src_address`, * FROM PATTERN[EVERY A=GlobalEvent(event_name='A')->(B=GlobalEvent(event_name='B') WHERE timer:within(20 min)) WHILE (A.occur_time <=B.occur_time AND B.occur_time - A.occur_time <=600000)];  //WrapperEventBean,MapEventBean
```

无需额外添加*，规则已有。
Listener中，select内容是放在一个WrapperEventBean对象中，*引用的几个日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。

#### 关联类模板: or-follow-by

```sql
SELECT A.`dst_address` AS `dst_address`, * FROM PATTERN[(EVERY A=GlobalEvent(event_name='A')->(B=GlobalEvent(event_name='B' AND (A.`src_address`=B.`src_address`)) WHERE timer:within(10 min))) OR (EVERY A=GlobalEvent(event_name='B')->(B=GlobalEvent(event_name='A' AND (A.`src_address`=B.`src_address`)) WHERE timer:within(10 min)))]  //WrapperEventBean,MapEventBean
```

无需额外添加*，规则已有。
Listener中，select内容是放在一个WrapperEventBean对象中，*引用的两个日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。

#### 关联类模板: not-follow-by

```sql
SELECT A.`src_address` AS `src_address`, * FROM PATTERN[EVERY A=GlobalEvent(event_name='A') -> (timer:interval(1 sec) AND NOT B=GlobalEvent(event_name='B'))];   //WrapperEventBean,MapEventBean
```

<font color='red'>需额外添加*。</font>
Listener中，select内容是放在一个WrapperEventBean对象中，*引用的日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。

#### 关联类模板: repeat-until

```sql
SELECT A[0].`src_address` AS `src_address`, B.`dst_address` AS `dst_address`, * FROM PATTERN[EVERY [2] A=GlobalEvent(event_name='A')->(B=GlobalEvent(event_name='B') WHERE timer:within(20 min)) WHILE (A[0].occur_time <=B.occur_time AND B.occur_time - A[0].occur_time <=600000)];   //WrapperEventBean,MapEventBean
```

无需额外添加*，规则已有。
Listener中，select内容是放在一个WrapperEventBean对象中，*引用的多个日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。取最后一笔日志即可。

#### 关联类模板: not-before

```sql
SELECT B.`src_address` AS `src_address`, * FROM PATTERN[EVERY (A=GlobalEvent(setActiveTime('25', A, 'occur_time') AND updateNbfState((event_name='A'), '25', A, 'occur_time', 'src_address')) OR B=GlobalEvent(isNotBefore((event_name='B'), '25', B, 'occur_time', 60, 'src_address')))];   //WrapperEventBean,MapEventBean
```

<font color='red'>需额外添加*。</font>
Listener中，select内容是放在一个WrapperEventBean对象中，*引用的日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。取B事件即可。

#### 关联类模板: any-order

```sql
SELECT irstream * FROM GlobalEvent(onCase((event_name='A'), 'I1HSC04F0011', 0, 2, *, 'src_address') OR onCase((event_name='B'), 'I1HSC04F0011', 1, 2, *, 'src_address')).win:ext_timed(occur_time, 10 min) HAVING (TRUE)   //WrapperEventBean,MapEventBean
```

无需额外添加*，规则已有。
初始Listener会将所有数据封装成WrapperEventBean传给内嵌Listener，*引用的多个日志可以通过((WrapperEventBean) eventBean).getUnderlyingEvent().getUnderlying()方法拿到。取最后一笔日志即可。

#### 关联类模板: not-occur

不关联事件，无需改动。