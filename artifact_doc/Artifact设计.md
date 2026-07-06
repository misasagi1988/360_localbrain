## 实体定义

|   |   |
|---|---|
| 实体类型 | 来源  |
| 内网IP | 日志源地址、日志目的地址、日志主机IP，告警的hw_compromised_asset，告警的attacker_array/victim_array |
| 外网IP | 日志源地址、日志目的地址，告警的attacker_array/victim_array |
| 域名 | 日志域名，告警的attacker_array/victim_array |
| 样本HASH | 日志文件MD5、日志进程MD5 |
| 主机 | 日志客户端标识，告警的hw_compromised_asset |
| 账号 | EDR登录事件中账号信息、网络日志中账号信息，告警中的账号信息， |

## 实体分析

### 内网IP

提取过滤条件: 
```
SELECT src_address as intranet_ip, occur_time as occur_time FROM GlobalEvent(belongs(`src_address`, 'CSWLHT4101a6'));
SELECT dst_address as intranet_ip, occur_time as occur_time FROM GlobalEvent(belongs(`dst_address`, 'CSWLHT4101a6'));
SELECT host_ip as intranet_ip, host_name as host_name, client_host_sign as machine_id, occur_time as occur_time FROM GlobalEvent(belongs(`host_ip`, 'CSWLHT4101a6'))
```

### 外网IP

提取过滤条件: 
```
SELECT src_address as internet_ip, src_port as port, occur_time as occur_time FROM GlobalEvent(not belongs(`src_address`, 'CSWLHT4101a6'));
SELECT dst_address as internet_ip, dst_port as port, occur_time as occur_time FROM GlobalEvent(not belongs(`dst_address`, 'CSWLHT4101a6'))
```
行为分析: 

### 域名

提取过滤条件: 
```
SELECT domain_name as domain_name, occur_time as occur_time FROM GlobalEvent(domain_name is not null and not is_ipv4(`domain_name`))
```
行为分析: 

### 样本hash

提取过滤条件: 
```
SELECT file_md5 as hash, filename as name, file_signer as signer, file_path as path, threat_score as threat_score, any_nonnull(threat_identify_result, file_net_level) as net_level, malware_name as malware_name, occur_time as occur_time FROM GlobalEvent(`file_md5` is not null);  
SELECT proc_md5 as hash, proc_name as name, proc_signer as signer, proc_path as path, threat_score as threat_score, any_nonnull(threat_identify_result, proc_net_level) as net_level, malware_name as malware_name, occur_time as occur_time FROM GlobalEvent(`proc_md5` is not null)
```
行为分析: 

### 主机

提取过滤条件: 
```
SELECT client_host_sign as intranet_machine, host_name as host_name, src_mac as mac, host_ip as ip, os as operating_system, occur_time as occur_time FROM GlobalEvent(`client_host_sign` is not null)
```
行为分析: 

### 账号

提取过滤条件: 
```
SELECT user_name as user_name, data_source as data_source, event_level as event_level, organization_id_path as organization_id_path, occur_time as occur_time FROM GlobalEvent(event_name = '登录事件' and data_source in ("360EDR","360BDR","360EPP") and user_name not in ("root", "admin", "administrator", "guest", "Root", "Admin", "Administrator", "Guest"));  
SELECT user_name as user_name, data_source as data_source, event_level as event_level, organization_id_path as organization_id_path, occur_time as occur_time FROM  GlobalEvent(event_name = '网络攻击' and user_name not in ("root", "admin", "administrator", "guest", "Root", "Admin", "Administrator", "Guest"));
SELECT user_name as user_name, data_source as data_source, alarm_level + 1 as event_level, 1 as source, organization_id_path_array as organization_id_path, start_time as occur_time FROM GlobalAlarm(`user_name` is not null and user_name not in ("root", "admin", "administrator", "guest", "Root", "Admin", "Administrator", "Guest"))
```

行为分析: 


### 威胁图谱绘制相关

```
artifact_aggregate:  
  #内网IP之间互相访问  
  intranet_to_intranet_index_prefix: 7ae45eda14eab4739627bfaa92fe2bb1  
  #内网IP访问外网IP  
  intranet_to_internet_index_prefix: 1f49743bbc7d3b4a5b749c5d0384a474  
  #外网IP访问内网IP  
  internet_to_intranet_index_prefix: 85a95eff1bbf52a06d281c6087a2cb19  
  #内网IP访问域名  
  intranet_to_domain_index_prefix: 27e85b3f565dcf8f0e33e46afc32aefa  
  #访问主机的其他内网IP  
  intranet_to_machine_index_prefix: bb92be1a247850e1993c0dcb89da02a1  
  #外网IP主动访问端口分布  
  internet_to_port_index_prefix: bb68a3c34ab5920a263fd33220e26696  
  #外网IP主动访问域名分布 e3bcf83eb128a1592327b7f5be1eebcf  
  internet_to_domain_index_prefix: e3bcf83eb128a1592327b7f5be1eebcf  
  #对域名的端口访问分布  
  domain_to_port_index_prefix: 60a7430cad6f996bdb00fd2f9ff33751  
  #访问该域名的主机分布  
  domain_to_host_index_prefix: 631270ebe0333f2313da9fad812aad78  
  #intranet 本机发起网络事件分布  
  intranet_to_event_index_prefix: 6b2346d31d7aa10372bd5fdbb69f53ec  
  #intranet 连接本机网络事件分布  
  to_intranet_event_index_prefix: 31e609db356aa33f4ff4367501685cd9  
  #internet 外网IP发起网络事件分布  
  internet_to_event_index_prefix: ff9c7c910448e2bdc8dbcb2386ac939b  
  #-- 外网IP绑定域名 22d83e16e27e468b3d4111ea1bdcc7c3  
  internet_bind_domain_index_prefix: 22d83e16e27e468b3d4111ea1bdcc7c3  
  #internet 连接外网IP网络事件分布  
  to_internet_event_index_prefix: 6a56be01456cf9a04c5e8cd5e9f9ecbf  
  #intranet 内网IP开放端口（内网）67fad221878a6b219877866848ef3b79  
  to_intranet_port_intranet_index_prefix: 67fad221878a6b219877866848ef3b79  
  #intranet 内网IP开放端口（外网）635b42388696ad93c64e4e9a513adc0b  
  to_intranet_port_internet_index_prefix: 635b42388696ad93c64e4e9a513adc0b  
  #artifact-rules-file.yml Hash在内网主机分布 a1e48ec2ca22887c52ddfc98fcea640e 文件名或者进程名name  
  hash_dist_host_index_prefix: a1e48ec2ca22887c52ddfc98fcea640e  
  #artifact-rules-file.yml 文件分布 8a7aabf5ca6efd75cf839b0daf449459 取host_ip 分布主机  
  hash_file_dist_index_prefix: 8a7aabf5ca6efd75cf839b0daf449459  
  #d76ffcae137928005321c613f86df10f 该Hash访问的目的内网IP  
  hash_file_to_intranet_ip_index_prefix: d76ffcae137928005321c613f86df10f  
  #d45cd57e100eca3a515ef1c5f7a018a5 Hash访问外网IP  
  hash_file_to_internet_ip_index_prefix: d45cd57e100eca3a515ef1c5f7a018a5  
  #d8af28cde450ee7345f179f2a6c8be6a 进程的操作 event_name  hash_file_op_process_index_prefix: d8af28cde450ee7345f179f2a6c8be6a  
  #b8fa719b31334c3be40b95af1314b67c Hash访问外网域名  
  hash_file_to_internet_domain_prefix: b8fa719b31334c3be40b95af1314b67c  
  # a1e48ec2ca22887c52ddfc98fcea640e Hash在内网主机分布  
  hash_file_dist_intranet_prefix: f371aca50c47f3bea81a08bcc4d09386  
  #进程链 该Hash的常见父（子）进程 faa051c220ea4cf93b4d8963444c3543  proc_to_proc_index_prefix: faa051c220ea4cf93b4d8963444c3543  
  # 账号登录内网IP 8ae8dd1e83087b76d44f4c5c72bed190  
  account_to_intranet_index_prefix: 8ae8dd1e83087b76d44f4c5c72bed190  
  # 主机访问的外网域名 c8decd5ac47d58649249a3b06eb7d565  machine_to_domain_index_prefix: c8decd5ac47d58649249a3b06eb7d565  
  # 主机访问的外网IP c6085481337d4641d9570ae5f6d2be5a  
  machine_to_internet_index_prefix: c6085481337d4641d9570ae5f6d2be5a  
  #主机使用的内网IP  
  machine_bind_intranet_index_prefix: 6cfc5910a2323a52e502c04fb3f02f76  
  # 访问该外网IP的内网主机 64cef5874650675c5eb87a6a88da04c7  intranet_machine_to_internet: 64cef5874650675c5eb87a6a88da04c7  
  # 访问主机的外网IP c415ca50877cc23249b0515c58364a68  
  internet_to_machine_index_prefix: c415ca50877cc23249b0515c58364a68  
  # 用户登录本机 485ed11b9f1b65d847e23287a1460e6a  user_to_host_index_prefix: 485ed11b9f1b65d847e23287a1460e6a
```