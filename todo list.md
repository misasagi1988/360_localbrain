

1. 选几个感兴趣的模块负责，做owner: shuri+shuri-master(情报，回扫相关)，analysis(旁路分析，规则评估，数据源评估)， 人行上报
2. ip lib 更新，尝试用geo lib替换, [https://dev.maxmind.com/geoip/geolite2-free-geolocation-data](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
3. UEBA异常场景构建，尝试用angler规则配置出来(基线类，用户登录时间异常，用户登录)
a)通过历史数据自学习能自动生成服务器行为基线，再对比行为基线识别异常行为，包括但不限于源IP与目的IP的异常访问关系、源IP与目的端口的异常访问关系、源IP与目的IP的异常访问次数等。  
b)通过历史数据自学习能自动生成用户行为基线，再对比行为基线识别异常行为，包括但不限于用户登录异常、用户操作次数异常、用户操作时间异常等。



建议: 情报、回扫、规则评估、 compliance、重保任务、人行上报也可以，都比较独立


GEOIP的报价问题
所有组件默认使用G1GC
hes-sae-group-0的partition最好是偶数（6）
信息组转换的正则（^$）
shuri情报匹配接口性能有问题


GeoLite2:
环境变量：GEO_DB_PATH
本脑目前使用的是IP_city_single_WGS84.awdb
应用模块：
artifact/incident/dv/tomcat