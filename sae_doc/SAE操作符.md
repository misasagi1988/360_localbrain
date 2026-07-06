# SAE操作符

标签（空格分隔）： SAE_DOC

---
字段类型：
每个类型可以细分有数组/非数组类型。

| 操作符 | 支持字段类型   |  esper自定义函数 | 引擎方法  |  样例  |
| --------   | :-----  | :----  | :----  | :----  |
| =  | 关系操作符，各种非数组类型都支持，支持V/F | esper原生，=，ip类型有做特殊处理  | =  |  event_name = 'web访问' |
| !=  | 关系操作符，各种非数组类型都支持，支持V/F | esper原生，!=，ip类型有做特殊处理  | !=  |  event_name != 'web访问' |
| >  | 关系操作符，各种非数组类型都支持，支持V/F | 非ip类型esper原生，>，ip类型有做特殊处理 | >，ipValueCompare   |  src_port > 8080L |
| >=  | 关系操作符，各种非数组类型都支持，支持V/F | 非ip类型esper原生，>=，ip类型有做特殊处理  | >=，ipValueCompare |  src_port >= 8080L |
| <  | 关系操作符，各种非数组类型都支持，支持V/F | 非ip类型esper原生，<，ip类型有做特殊处理 | <，ipValueCompare  |  src_port < 8080L |
| <=  | 关系操作符，各种非数组类型都支持，支持V/F | 非ip类型esper原生，<=，ip类型有做特殊处理 | <=，ipValueCompare  |  src_port <= 8080L |
| like  | 字符串忽略大小写包含，左值支持字符及字符数组类型，如果左值为字符串数组，只要数组的任意元素包含该字符串即可匹配。支持V/F |  contains | contains  |  contains(event_name, 'web') |
| plike  | 字符串忽略大小写起始包含，左值支持字符及字符数组类型，如果左值为字符串数组，只要数组的任意元素起始包含该字符串即可匹配。支持V/F |  prefixContains | prefixContains  |  prefixContains(event_name, 'web') |
| rlike  | 字符串正则匹配，忽略大小写，点号支持匹配换行符，仅支持字符类型属性，特殊字符需转义。 |  esper原生，regexp  | regexp |  proc_path regexp '.*\\\\cmd.exe' |
| exist  | 存在，无右操作数，支持任意类型属性，可用于过滤条件。 |  esper原生，is not null | is not null  | src_address is not null  |
| not_exist  | 不存在，无右操作数，支持任意类型属性，可用于过滤条件。 |  esper原生，is null | is null  | dst_address is null  |
| belong  | 属于特征，右操作数仅支持F，用于匹配安全信息和动态信息。 安全信息中，字符类信息细分为字符串比较/正则全匹配/正则部分匹配三种子类型： 字符串比较是用事件的字段值与该信息组的内容做比较，只要该事件的字段值与该信息组的任一内容相等即可(大小写敏感)； 正则全匹配类型是用事件的字段值与该信息组的内容做正则模式全匹配，只要该事件的字段值能够完全匹配该信息组的任一正则表达式即可(忽略大小写)； 正则部分匹配类型是用事件的字段值与该信息组的内容做正则模式部分匹配，只要该事件的字段值能够部分匹配该信息组的任一正则表达式即可(忽略大小写)。 正则类安全信息，.支持匹配换行符。正则类、ip类信息组对规则处理性能影响较大，配置时注意后移。可用于过滤条件。 | belongs  | objectCheck |  belongs(src_address, 'CSWLHT4101a6') |
| contain  | 左操作数仅支持数组类型，数组元素可为任意类型，数组任意元素内容与右值相同即可匹配，字符类属性大小写敏感，支持V/F |  esper原生，in  | in | 'c2' in (ti_tags)  |
| in  | 支持IP及数组格式字符串"[xxx]"。 IP：左操作数属于网段；数组格式字符串：数组的元素包含左操作数。 支持V。 |  IP: ipExist; 数组格式字符串：in | ipExist: ipExist | ipExist(src_address, '(10.16.0.0/16)')  |
| match  | 匹配威胁情报，无右操作数，仅针对源地址/目的地址/域名/URL/文件MD5/进程MD5字段有效。指明具体是哪个字段匹配到了情报。可用于过滤条件。 |  = | =  | spin_tag=2/3/4/5/6/7   |
| inmap  | 匹配多维信息组，多维信息组的key和value仅支持单个值，不支持区间格式。右操作数为信息组名称.字段名称格式，可用于过滤条件。demo: 源地址 inmap 多维信息组测试.目的地址，目的地址是多维信息组的键，且源地址在目的地址对应多维信息组键的值的set里。即key&value都匹配。 |  inmap | inMap  | inmap('00VFHPF60013', dst_address, src_address) |
| not_inmap  | 匹配多维信息组，多维信息组的key和value仅支持单个值，不支持区间格式。右操作数为信息组名称.字段名称格式，可用于过滤条件。demo: 源地址 not_inmap 多维信息组测试.目的地址，目的地址是多维信息组的键，且源地址不在目的地址对应多维信息组键的值的set里。即key匹配，value不匹配。 |  not_inmap | notInMap  | not_inmap('00VFHPF60013', dst_address, src_address) |


###  4.0版本新增

=/!= 操作符，左值支持数组类型，类似contain处理逻辑
数组字段 `in` 操作符转换为 `contain` 操作符

### 4.5版本新增

contain操作符支持 contain [...] 格式，左值为数组类型，对应引擎方法为anyMatch，表示，右边数组包含左操作数的任意元素即可满足条件。=/!= 操作符对于左值为数组类型的，也有类似功能
