标签（空格分隔）： 本脑v4.5版本，2025

---

环境变量PRIMARY_LANGUAGE指明了当前的语言环境

### tomcat后端改造
##### geo富化改造
geo英文awdb放入标品build，可以根据语言配置解压对应awdb文件；
流水线改造，合入英文awdb；安装脚本改造，根据语言配置选择awdb解压；
ipplus公共依赖优化，支持英文awdb，放到依赖仓库。只更新了代码，没有做版本升级
##### shuri情报匹配
情报匹配事件名称改造，情报回扫相关改动
##### attack_insight改造
接口适配i18n
配置文件，各种专项场景fliter，适配i18n
各个枚举字段映射，适配i18n
##### xdr改造
接口适配i18n
旁路分析适配i18n   ---暂未做

### 数据表改造
##### database-mgr各个数据表初始化
利用大模型，提取数据表对应字段，更新sql，字段改为key=value格式，中文提取，英文翻译。更新的数据表有：security_intelligence_group/security_event_base/attack_scene/ds_compliance_module/global_constant_mapping/province_city_area/system_config/security_domain_info/search_fields_template/sae_branch_group/white_alarm_group/custom_navigation/notification_policy_rule/xdr_type/attack_scene/system_entity/monitor_class/monitor_type/monitor_alarm_strategy等。感触最深的是ds_compliance_module数据表，721项，多个字段需要翻译，几个字段中文很长，跟kimi对话每次数量不能超过20w，每次对话时间都过长，还没做完就会过期，要多次让它接着做。最终想到的策略是sql语句自己脚本生成，它只做字段提取，中文和英文i18n文本生成的操作。如果人工操作的话预估一周都不会干完，出错概率也会很高，而采用大模型帮忙，只用了1天即完成。
翻译后，部分数据表字段长度有限制，翻译为英文后因长度问题导致数据无法正常写入，最终通过更新安装脚本init_data.sh自测更新后的sql文件，成功实现导入。


##### 信息组类型相关
```
update security_intelligence_group set name = 'Information Management', name_path = '/Information Management' WHERE id = '4EOBUIG80010';
update security_intelligence_group set name = 'IP Information', name_path = '/Information Management/IP Information' WHERE id = '4EOBUIG80011';
update security_intelligence_group set name = 'Numeric Information', name_path = '/Information Management/Numeric Information' WHERE id = '4EOBUIG80012';
update security_intelligence_group set name = 'Character Information', name_path = '/Information Management/Character Information' WHERE id = '4EOBUIG80013';
update security_intelligence_group set name = 'Time Information', name_path = '/Information Management/Time Information' WHERE id = '4EOBUIG80014';
update security_intelligence_group set name = 'Key-Value Pair Information', name_path = '/Information Management/Key-Value Pair Information' WHERE id = '4EOBUIG80015';
UPDATE security_intelligence_group SET name_path = CONCAT('/Information Management/IP Information/', SUBSTRING(name_path, CHAR_LENGTH('/信息管理/IP类信息/') + 1)) WHERE name_path LIKE '/信息管理/IP类信息/%';
UPDATE security_intelligence_group SET name_path = CONCAT('/Information Management/Numeric Information/', SUBSTRING(name_path, CHAR_LENGTH('/信息管理/数字类信息/') + 1)) WHERE name_path LIKE '/信息管理/数字类信息/%';
UPDATE security_intelligence_group SET name_path = CONCAT('/Information Management/Character Information/', SUBSTRING(name_path, CHAR_LENGTH('/信息管理/字符类信息/') + 1)) WHERE name_path LIKE '/信息管理/字符类信息/%';
UPDATE security_intelligence_group SET name_path = CONCAT('/Information Management/Time Information/', SUBSTRING(name_path, CHAR_LENGTH('/信息管理/时间类信息/') + 1)) WHERE name_path LIKE '/信息管理/时间类信息/%';
UPDATE security_intelligence_group SET name_path = CONCAT('/Information Management/Key-Value Pair Information/', SUBSTRING(name_path, CHAR_LENGTH('/信息管理/键值对信息/') + 1)) WHERE name_path LIKE '/信息管理/键值对信息/%';
//还有前缀是内部信息管理的，也要更新
```
##### 事件名称相关
```
update security_event_base set event_name = 'Threat Intelligence IP Matching Event' where id = 'CIYII3AY0025';
update security_event_base set event_name = 'Threat Intelligence Domain Matching Event' where id = 'GTMCKZN50026';
update security_event_base set event_name = 'Threat Intelligence URL Matching Event' where id = 'BRG1H1Q20027';
update security_event_base set event_name = 'Threat Intelligence HASH Matching Event' where id = 'PKQV7FQG000f';
update security_event_base set event_name = 'Exploit Matching Event' where id = 'GRPL7X4Q0022';
```
##### attack_scene告警类型
```
INSERT INTO `attack_scene` (`id`, `parent_id`, `name`, `id_path`, `description`, `scene_type`, `scene_model`) VALUES
('4UTW9OGX0026', NULL, 'Scanning and Probing', '/4UTW9OGX0026', 'Scanning and Probing', 'ndr', 'network'),
('0OAW7H6M0048', '4UTW9OGX0026', 'Application Scanning', '/4UTW9OGX0026/0OAW7H6M0048', 'Application Scanning', 'ndr', 'network'),
('77HGWUHL004d', '4UTW9OGX0026', 'Network Scanning', '/4UTW9OGX0026/77HGWUHL004d', 'Network Scanning', 'ndr', 'network'),
('7Q8NO6GL004c', '4UTW9OGX0026', 'Email Scanning', '/4UTW9OGX0026/7Q8NO6GL004c', 'Email Scanning', 'ndr', 'network'),
('EZBB15BT004b', '4UTW9OGX0026', 'Host Scanning', '/4UTW9OGX0026/EZBB15BT004b', 'Host Scanning', 'ndr', 'network'),
('KI475EQJ0049', '4UTW9OGX0026', 'Vulnerability Scanning', '/4UTW9OGX0026/KI475EQJ0049', 'Vulnerability Scanning', 'ndr', 'network'),
('P1PRXX08004a', '4UTW9OGX0026', 'Service Scanning', '/4UTW9OGX0026/P1PRXX08004a', 'Service Scanning', 'ndr', 'network'),
('P1PRXX08004b', '4UTW9OGX0026', 'Other Scanning and Probing', '/4UTW9OGX0026/P1PRXX08004b', 'Other Scanning and Probing', 'ndr', 'network'),
('51BEMIBR0030', NULL, 'Host Anomaly', '/51BEMIBR0030', 'Host Anomaly', 'edr', 'process'),
('BEEMZD130067', '51BEMIBR0030', 'Container Anomaly', '/51BEMIBR0030/BEEMZD130067', 'Container Anomaly', 'edr', 'process'),
('CGRWD38V0069', '51BEMIBR0030', 'Script Anomaly', '/51BEMIBR0030/CGRWD38V0069', 'Script Anomaly', 'edr', 'process'),
('COU87UMX006a', '51BEMIBR0030', 'Registry Anomaly', '/51BEMIBR0030/COU87UMX006a', 'Registry Anomaly', 'edr', 'registry'),
('DKUQB91R006d', '51BEMIBR0030', 'Process Anomaly', '/51BEMIBR0030/DKUQB91R006d', 'Process Anomaly', 'edr', 'process'),
('FMBGXO7M0065', '51BEMIBR0030', 'Vulnerability Exploitation', '/51BEMIBR0030/FMBGXO7M0065', 'Vulnerability Exploitation', 'edr', 'process'),
('GI84I9M3006b', '51BEMIBR0030', 'File Anomaly', '/51BEMIBR0030/GI84I9M3006b', 'File Anomaly', 'edr', 'file'),
('POAW37H80068', '51BEMIBR0030', 'Driver Anomaly', '/51BEMIBR0030/POAW37H80068', 'Driver Anomaly', 'edr', 'process'),
('W4KNXXB10008', '51BEMIBR0030', 'Service Anomaly', '/51BEMIBR0030/W4KNXXB10008', 'Service Anomaly', 'edr', 'process'),
('WR4KG0UG006c', '51BEMIBR0030', 'Network Anomaly', '/51BEMIBR0030/WR4KG0UG006c', 'Network Anomaly', 'edr', 'network'),
('WR4KG0UG006d', '51BEMIBR0030', 'Other Host Anomaly', '/51BEMIBR0030/WR4KG0UG006d', 'Other Host Anomaly', 'edr', 'network'),
('52BV8871002b', NULL, 'Abnormal Communication', '/52BV8871002b', 'Abnormal Communication', 'ndr', 'network'),
('4Z8CMPBK0053', '52BV8871002b', 'Traffic Proxy', '/52BV8871002b/4Z8CMPBK0053', 'Traffic Proxy', 'ndr', 'network'),
('EXRQECYO0055', '52BV8871002b', 'Covert Tunnel', '/52BV8871002b/EXRQECYO0055', 'Covert Tunnel', 'ndr', 'network'),
('KPQDOAQH0056', '52BV8871002b', 'APT Communication', '/52BV8871002b/KPQDOAQH0056', 'APT Communication', 'ndr', 'network'),
('P7C18FN90052', '52BV8871002b', 'Reverse Shell', '/52BV8871002b/P7C18FN90052', 'Reverse Shell', 'ndr', 'network'),
('R7CVIBLF0051', '52BV8871002b', 'Malware Communication', '/52BV8871002b/R7CVIBLF0051', 'Malware Communication', 'ndr', 'network'),
('UH9WLG1I0054', '52BV8871002b', 'Remote Tools', '/52BV8871002b/UH9WLG1I0054', 'Remote Tools', 'ndr', 'network'),
('UH9WLG1I0055', '52BV8871002b', 'Denial of Service', '/52BV8871002b/UH9WLG1I0055', 'Denial of Service', 'ndr', 'network'),
('UH9WLG1I0056', '52BV8871002b', 'Man-in-the-Middle Attack', '/52BV8871002b/UH9WLG1I0056', 'Man-in-the-Middle Attack', 'ndr', 'network'),
('UH9WLG1I0057', '52BV8871002b', 'Other Abnormal Communication', '/52BV8871002b/UH9WLG1I0057', 'Other Abnormal Communication', 'ndr', 'network'),
('87E0FZ9X002d', NULL, 'Vulnerability Attack', '/87E0FZ9X002d', 'Vulnerability Attack', 'ndr', 'network'),
('UH9WLG1I008h', '87E0FZ9X002d', 'Vulnerability Attack', '/87E0FZ9X002d/UH9WLG1I008h', 'Vulnerability Attack', 'ndr', 'network'),
('ADVGAGT90031', NULL, 'Operations Monitoring', '/ADVGAGT90031', 'Operations Monitoring', 'edr', 'process'),
('AKG5U5IK0062', 'ADVGAGT90031', 'Performance Monitoring', '/ADVGAGT90031/AKG5U5IK0062', 'Performance Monitoring', 'edr', 'process'),
('DWNIZFOU0063', 'ADVGAGT90031', 'Fault Monitoring', '/ADVGAGT90031/DWNIZFOU0063', 'Fault Monitoring', 'edr', 'process'),
('PJ5AUEGA0064', 'ADVGAGT90031', 'Operation Audit', '/ADVGAGT90031/PJ5AUEGA0064', 'Operation Audit', 'edr', 'process'),
('PJ5AUEGA0065', 'ADVGAGT90031', 'Other Operations Monitoring', '/ADVGAGT90031/PJ5AUEGA0065', 'Other Operations Monitoring', 'edr', 'process'),
('BWMSFANW0025', NULL, 'Web Attack', '/BWMSFANW0025', 'Web Attack', 'ndr', 'network'),
('08X1LZ530046', 'BWMSFANW0025', 'Web Scanning', '/BWMSFANW0025/08X1LZ530046', 'Web Scanning', 'ndr', 'network'),
('14DW86FC0045', 'BWMSFANW0025', 'Web Crawling', '/BWMSFANW0025/14DW86FC0045', 'Web Crawling', 'ndr', 'network'),
('14DW86FC0046', 'BWMSFANW0025', 'SQL Injection', '/BWMSFANW0025/14DW86FC0046', 'SQL Injection', 'ndr', 'network'),
('2I2863S40038', 'BWMSFANW0025', 'Command Execution', '/BWMSFANW0025/2I2863S40038', 'Command Execution', 'ndr', 'network'),
('3TUIR73P0040', 'BWMSFANW0025', 'Misconfiguration', '/BWMSFANW0025/3TUIR73P0040', 'Misconfiguration', 'ndr', 'network'),
('6ZEKB75T003e', 'BWMSFANW0025', 'Directory Traversal', '/BWMSFANW0025/6ZEKB75T003e', 'Directory Traversal', 'ndr', 'network'),
('7A4KGSJK0043', 'BWMSFANW0025', 'Weak Password', '/BWMSFANW0025/7A4KGSJK0043', 'Weak Password', 'ndr', 'network'),
('98F4IVDA0033', 'BWMSFANW0025', 'Other Injection', '/BWMSFANW0025/98F4IVDA0033', 'Other Injection', 'ndr', 'network'),
('AE4AZ4EQ003c', 'BWMSFANW0025', 'Information Leakage', '/BWMSFANW0025/AE4AZ4EQ003c', 'Information Leakage', 'ndr', 'network'),
('C82ZNERM003a', 'BWMSFANW0025', 'Cross-Site Request Forgery', '/BWMSFANW0025/C82ZNERM003a', 'Cross-Site Request Forgery', 'ndr', 'network'),
('EN3WHGYI0044', 'BWMSFANW0025', 'Phishing', '/BWMSFANW0025/EN3WHGYI0044', 'Phishing', 'ndr', 'network'),
('EVSN114X0034', 'BWMSFANW0025', 'XSS Attack', '/BWMSFANW0025/EVSN114X0034', 'XSS Attack', 'ndr', 'network'),
('HFNEV6YO0042', 'BWMSFANW0025', 'Password Reset', '/BWMSFANW0025/HFNEV6YO0042', 'Password Reset', 'ndr', 'network'),
('I6O2SWM30047', 'BWMSFANW0025', 'Sensitive Information Reconnaissance', '/BWMSFANW0025/I6O2SWM30047', 'Sensitive Information Reconnaissance', 'ndr', 'network'),
('QBG1FZ2U003d', 'BWMSFANW0025', 'Code Execution', '/BWMSFANW0025/QBG1FZ2U003d', 'Code Execution', 'ndr', 'network'),
('TLU7GHXW0035', 'BWMSFANW0025', 'Webshell', '/BWMSFANW0025/TLU7GHXW0035', 'Webshell', 'ndr', 'network'),
('V3RZES470037', 'BWMSFANW0025', 'Directory Traversal', '/BWMSFANW0025/V3RZES470037', 'Directory Traversal', 'ndr', 'network'),
('W1P4T2FH003b', 'BWMSFANW0025', 'Unauthorized Access', '/BWMSFANW0025/W1P4T2FH003b', 'Unauthorized Access', 'ndr', 'network'),
('XF74TWI80041', 'BWMSFANW0025', 'File Writing', '/BWMSFANW0025/XF74TWI80041', 'File Writing', 'ndr', 'network'),
('XWD5OND9003f', 'BWMSFANW0025', 'Authentication Bypass', '/BWMSFANW0025/XWD5OND9003f', 'Authentication Bypass', 'ndr', 'network'),
('Y6GO7FCT0039', 'BWMSFANW0025', 'File Inclusion', '/BWMSFANW0025/Y6GO7FCT0039', 'File Inclusion', 'ndr', 'network'),
('ZDTVDOF30036', 'BWMSFANW0025', 'File Upload', '/BWMSFANW0025/ZDTVDOF30036', 'File Upload', 'ndr', 'network'),
('ZDTVDOF30037', 'BWMSFANW0025', 'File Reading', '/BWMSFANW0025/ZDTVDOF30037', 'File Reading', 'ndr', 'network'),
('ZDTVDOF30038', 'BWMSFANW0025', 'Web Page Tampering', '/BWMSFANW0025/ZDTVDOF30038', 'Web Page Tampering', 'ndr', 'network'),
('ZDTVDOF30039', 'BWMSFANW0025', 'Other Web Attack', '/BWMSFANW0025/ZDTVDOF30039', 'Other Web Attack', 'ndr', 'network'),
('QCLJR2VL002f', NULL, 'Network Attack', '/QCLJR2VL002f', 'Network Attack', 'ndr', 'network'),
('QCLJR2VL005y', 'QCLJR2VL002f', 'Network Attack', '/QCLJR2VL002f/QCLJR2VL005y', 'Network Attack', 'ndr', 'network'),
('QCLJR2VL002e', NULL, 'Account Anomaly', '/QCLJR2VL002e', 'Account Anomaly', 'ndr', 'network'),
('12CI5OXN005e', 'QCLJR2VL002e', 'Account Status Anomaly', '/QCLJR2VL002e/12CI5OXN005e', 'Account Status Anomaly', 'ndr', 'network'),
('2AC7OQYU005c', 'QCLJR2VL002e', 'Account Weak Password', '/QCLJR2VL002e/2AC7OQYU005c', 'Account Weak Password', 'ndr', 'network'),
('FD4CMH7W005f', 'QCLJR2VL002e', 'Brute Force Attack', '/QCLJR2VL002e/FD4CMH7W005f', 'Brute Force Attack', 'ndr', 'network'),
('YDKAGSFH005d', 'QCLJR2VL002e', 'Login Anomaly', '/QCLJR2VL002e/YDKAGSFH005d', 'Login Anomaly', 'ndr', 'network'),
('YDKAGSFH005e', 'QCLJR2VL002e', 'Other Account Anomaly', '/QCLJR2VL002e/YDKAGSFH005e', 'Other Account Anomaly', 'ndr', 'network'),
('QCLJR2VL002g', NULL, 'Threat Intelligence', '/QCLJR2VL002g', 'Threat Intelligence', 'ndr', 'network'),
('QCLJR2VL007h', 'QCLJR2VL002g', 'Threat Intelligence', '/QCLJR2VL002g/QCLJR2VL007h', 'Threat Intelligence', 'ndr', 'network'),
('XDFP8EHM002f', NULL, 'Email Attack', '/XDFP8EHM002f', 'Email Attack', 'ndr', 'network'),
('IH3ROERU0061', 'XDFP8EHM002f', 'Phishing Email', '/XDFP8EHM002f/IH3ROERU0061', 'Phishing Email', 'ndr', 'network'),
('QPIVA2610060', 'XDFP8EHM002f', 'Spam Email', '/XDFP8EHM002f/QPIVA2610060', 'Spam Email', 'ndr', 'network'),
('QPIVA2610061', 'XDFP8EHM002f', 'Other Email Attack', '/XDFP8EHM002f/QPIVA2610061', 'Other Email Attack', 'ndr', 'network'),
('XDFP8EHM002g', NULL, 'Multi-Dimensional Correlation', '/XDFP8EHM002g', 'Multi-Dimensional Correlation', 'ndr', 'network'),
('XDFP8EHM001g', 'XDFP8EHM002g', 'Multi-Dimensional Correlation', '/XDFP8EHM002g/XDFP8EHM001g', 'Multi-Dimensional Correlation', 'ndr', 'network'),
('XDFP8EHM002i', NULL, 'Content Security', '/XDFP8EHM002i', 'Content Security', 'ndr', 'network'),
('QPIVA2610066', 'XDFP8EHM002i', 'Content Change', '/XDFP8EHM002i/QPIVA2610066', 'Content Change', 'ndr', 'network'),
('QPIVA2610067', 'XDFP8EHM002i', 'Harmful Content', '/XDFP8EHM002i/QPIVA2610067', 'Harmful Content', 'ndr', 'network'),
('QPIVA2610068', 'XDFP8EHM002i', 'Sensitive Content', '/XDFP8EHM002i/QPIVA2610068', 'Sensitive Content', 'ndr', 'network'),
('QPIVA2610069', 'XDFP8EHM002i', 'Non-compliant Content', '/XDFP8EHM002i/QPIVA2610069', 'Non-compliant Content', 'ndr', 'network'),
('QPIVA2610070', 'XDFP8EHM002i', 'Other Content Security', '/XDFP8EHM002i/QPIVA2610070', 'Other Content Security', 'ndr', 'network'),
('T5Q3GBMT002b', NULL, 'Malicious Program', '/T5Q3GBMT002b', 'Malicious Program', 'ndr', 'network'),
('QPIVA2610071', 'T5Q3GBMT002b', 'BootKit Virus', '/T5Q3GBMT002b/QPIVA2610071', 'BootKit Virus', 'ndr', 'network'),
('QPIVA2610072', 'T5Q3GBMT002b', 'RootKit Virus', '/T5Q3GBMT002b/QPIVA2610072', 'RootKit Virus', 'ndr', 'network'),
('QPIVA2610073', 'T5Q3GBMT002b', 'Downloader', '/T5Q3GBMT002b/QPIVA2610073', 'Downloader', 'ndr', 'network'),
('QPIVA2610074', 'T5Q3GBMT002b', 'Ransomware', '/T5Q3GBMT002b/QPIVA2610074', 'Ransomware', 'ndr', 'network'),
('QPIVA2610075', 'T5Q3GBMT002b', 'Backdoor Program', '/T5Q3GBMT002b/QPIVA2610075', 'Backdoor Program', 'ndr', 'network'),
('QPIVA2610076', 'T5Q3GBMT002b', 'Macro Virus', '/T5Q3GBMT002b/QPIVA2610076', 'Macro Virus', 'ndr', 'network'),
('QPIVA2610077', 'T5Q3GBMT002b', 'Generic Trojan', '/T5Q3GBMT002b/QPIVA2610077', 'Generic Trojan', 'ndr', 'network'),
('QPIVA2610078', 'T5Q3GBMT002b', 'Adware', '/T5Q3GBMT002b/QPIVA2610078', 'Adware', 'ndr', 'network'),
('QPIVA2610079', 'T5Q3GBMT002b', 'Cryptojacking Malware', '/T5Q3GBMT002b/QPIVA2610079', 'Cryptojacking Malware', 'ndr', 'network'),
('QPIVA2610080', 'T5Q3GBMT002b', 'Infectious Virus', '/T5Q3GBMT002b/QPIVA2610080', 'Infectious Virus', 'ndr', 'network'),
('QPIVA2610081', 'T5Q3GBMT002b', 'Destructive Virus', '/T5Q3GBMT002b/QPIVA2610081', 'Destructive Virus', 'ndr', 'network'),
('QPIVA2610082', 'T5Q3GBMT002b', 'Information-stealing Trojan', '/T5Q3GBMT002b/QPIVA2610082', 'Information-stealing Trojan', 'ndr', 'network'),
('QPIVA2610083', 'T5Q3GBMT002b', 'Banking Trojan', '/T5Q3GBMT002b/QPIVA2610083', 'Banking Trojan', 'ndr', 'network'),
('QPIVA2610084', 'T5Q3GBMT002b', 'Script Virus', '/T5Q3GBMT002b/QPIVA2610084', 'Script Virus', 'ndr', 'network'),
('QPIVA2610085', 'T5Q3GBMT002b', 'Worm Virus', '/T5Q3GBMT002b/QPIVA2610085', 'Worm Virus', 'ndr', 'network'),
('QPIVA2610086', 'T5Q3GBMT002b', 'Remote Control Trojan', '/T5Q3GBMT002b/QPIVA2610086', 'Remote Control Trojan', 'ndr', 'network'),
('QPIVA2610087', 'T5Q3GBMT002b', 'Spyware', '/T5Q3GBMT002b/QPIVA2610087', 'Spyware', 'ndr', 'network'),
('QPIVA2610088', 'T5Q3GBMT002b', 'Hacking Tools', '/T5Q3GBMT002b/QPIVA2610088', 'Hacking Tools', 'ndr', 'network'),
('QPIVA2610089', 'T5Q3GBMT002b', 'APT Virus', '/T5Q3GBMT002b/QPIVA2610089', 'APT Virus', 'ndr', 'network'),
('QPIVA2610090', 'T5Q3GBMT002b', 'Botnet', '/T5Q3GBMT002b/QPIVA2610090', 'Botnet', 'ndr', 'network'),
('QPIVA2610091', 'T5Q3GBMT002b', 'Other Malicious Program', '/T5Q3GBMT002b/QPIVA2610091', 'Other Malicious Program', 'ndr', 'network');
```
### XDR旁路分析

##### XDR旁路分析相关镜像

| 镜像 | 容器名称 | 模块名称 | 模块功能描述 |
| --- | --- | --- | --- |
| secstudy_rule_evaluation_img	 | secstudy_rule_evaluation	 | 规则评估 | 本脑sae规则评估及数据源评估 |
| kc_cloudapi_img | kc_cloudapi_service | 知识云CloudAPI离线服务 | 知识云CloudAPI离线服务提供典型的攻击场景及告警处置建议内容。目前提供了killchain和remediation两个接口，用于规则典型攻击场景展示和威胁告警的云端富化处置建议。 |
| log-assistant	 | 	log-assistant-service	 | log-assistant | 解析规则智能推荐 |

##### 多语言support

对镜像按语言分文件夹存在，zh_cn及en两个文件夹
根据环境的语言配置，初次启动初始化时，加载对应语言的镜像

### 依赖外部输出的问题记录
|   |   |
|---|---|
| 问题 | 说明  |
| IP GEO富化 | 当前awdb ip数据库不支持英文，也不支持ipv6。已咨询过客服，他们有全英的离线数据库 |
| shuri情报匹配富化 | 依赖情报 |
| 内容包APT相关 | 之前情报部门给的APT信息。内容比较少，格式也很规范，两个json文件，可尝试自行翻译 |