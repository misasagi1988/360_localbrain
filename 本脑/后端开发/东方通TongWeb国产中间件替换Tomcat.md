标签（空格分隔）： 国产中间件适配

---
tongweb版本：TongWeb8.0.9.04
部署环境: 11.123.244.208
部署目录: /opt/middleware/tongweb
tongweb管理控制台网页访问: 
http://11.123.244.208:9060/console
tongweb默认用户名/密码：thanos/thanos123.com
208环境密码: Q!hooS0c
wiki:  https://geelib.qihoo.net/geelib/knowledge/doc?spaceId=1384&docId=296680

### 部署思路

正常安装本脑tomcat，等待安装完毕后，将tomcat/webapps的所有应用通过TongWeb控制台部署到TongWeb上，停掉本脑tomcat，利用TongWeb加载tomcat所有应用，替代tomcat原有服务。

### 改动点:

1. 通道配置，8080，启用get/post/put/delete请求
2. tomcat相关环境变量:
GEO_DB_PATH
SOC_GLOBAL_CONFIG_DIR
TOMCAT_SHARE_DATA_DIR
LIC_PUBLIC_KEY
catalina.base，
3. log4j2.yml, log目录改动
root log4j2.yml log目录改动
sae log4j2.yml, log目录改动
ice log4j2.yml, log目录改动
4. 应用部署及启动
version.properties: 
docker cp lbrain-tomcat:/opt/qihoo/soc/tomcat/webapps/version.properties /${tongweb.home}/domains/version.properties
webapps:
docker cp lbrain-tomcat:/opt/qihoo/soc/tomcat/webapps  /${tongweb.home}/domains/
5. ROOT的tmp目录改动
backend.yml , spring.servlet.multipart.location: /opt/qihoo/soc/tomcat/temp
6. hqlite-client jar包适配
ice/ROOT hql-client.jar

### 东方通配置关注点:

#### tongweb基础配置

JVM配置: 内存配置，-e环境变量
启动参数: -D相关启动参数

#### 应用配置

应用的基础配置: 应用名、访问前缀、部署路径
应用资源加载: 开启使用TongWeb WebSocket开关，配置虚拟目录，虚拟目录类似于tomcat server.xml的Context标签，将指定的本地磁盘目录映射为 Tomcat 可访问的 Web 虚拟路径。静态资源访问逻辑，Tomcat 先匹配自身的 Context 路径映射（如 /report/downloads），匹配成功则直接读取 docBase 目录下的静态资源并返回，不经过 Spring 拦截；只有 Tomcat 无法匹配的路径，才会转发给 Spring DispatcherServlet 处理，如果找不到相关路径，抛NoHandlerFoundException异常。
==应用性能相关==: 强制从TongWeb加载静态资源，并指定由TongWeb加载的静态资源URL模式: -.ppt,-.pptx,-.pdf,-.xlsx,-.docx,-.doc,-.zip,-.html,-.txt,-.jpg,-.jpeg,-.png,-.gif,-.bmp,-.svg,-.ico,-.tif,-.tiff,-.webp,-.heif,-.heic,-.psd,-.raw,-.cr2,-.nef
应用资源加载及指定静态资源url模式建议同时配置。

##### 2026-02-10中再东方通下载失败问题探讨
中再5.0，下载文件接口遇到了点问题，在应用中配置了强制从TongWeb加载静态资源，并指定由TongWeb加载的静态资源URL模式，但有些下载接口也支持下载这些后缀的文件，这就导致下载接口无效了。分析看，有些静态资源和下载接口分不开了，导致下载接口失效。
改动方法：
启动参数中添加-Dcom.tongweb.web.static.resource.load.strategy=application_first
更新指定由TongWeb加载的静态资源URL模式：非那些后缀，更新为这些：/report/downloads/-,/dashboard/upload/-

#### 容器配置

通道配置，HTTP属性配置

### tongweb接口相关问题

最近在定制开发那边发现一个问题，接口存在，请求到后端是莫名其妙加了个.导致NoHandlerFoundException: no endpoint POST /work_orders/business/export.
定位这个点号是tongweb加的，豆包给的解释是：
核心根源：TongWeb 8.0.9.4 的「URL 后缀解析规则」
TongWeb 8.0.9.4 是基于老版本 Servlet 规范（Servlet 3.1/4.0） 开发的国产应用服务器，它对 URL 的解析逻辑有一个关键特性：
默认将 URL 按 . 分割为「文件名 + 后缀」，即使 URL 没有 .，也会尝试补全后缀或判定为「无后缀文件」。
具体到 /work_orders/business/export 这个路径：
TongWeb 会把最后一级 export 识别为「文件名」，且认为这个文件名缺少后缀；
为了适配传统 Web 应用的「静态资源解析逻辑」（比如 .html/.jsp），TongWeb 在内部处理时，会给这个「无后缀文件名」隐式补充一个空后缀的标记（表现为末尾加 .）；
这个加了 . 的路径（/export.）被转发给 Spring Boot 后，Spring 找不到匹配的 /export. 接口，就抛出 NoHandlerFoundException。

TongWeb 加 . 的逻辑是多层级优先级判定，参数只是 “弱缓解”，不是 “绝对屏蔽”：
第一优先级：路径层级 + 特征 → 决定是否触发静态文件误判
浅层级（≤4 级）+ 纯业务短单词（export/import）→ 优先判定为「静态文件」，无视参数，直接加 .；
深层级（≥5 级）+ 特殊字符（__/ 长随机串）→ 判定为「动态接口」，参数会进一步强化这个判定，不加 .。
第二优先级：参数 → 仅对 “边缘判定” 场景生效
比如路径是 /strategy/export（4 级），带参数可能让 TongWeb 犹豫，大概率不加 .；
但路径是 /business/export（3 级），属于 TongWeb 「强判定为静态文件」的场景，参数无法抵消这个判定，仍会加 .。

豆包给的兼容方案(attention: 没有试过)：
```
spring:
  mvc:
    # 路径匹配核心配置（适配 TongWeb 加 . 的关键）
    pathmatch:
      # 强制使用 AntPathMatcher（兼容 TongWeb 解析的路径，3.3 必须开）
      matching-strategy: ant_path_matcher
      # 显式禁用后缀模式匹配（忽略 TongWeb 加的 .，3.3 需配合 ant_path_matcher 才生效）
      use-suffix-pattern: false
      # 禁用注册后缀匹配（防止仅匹配 .json/.xml 等注册后缀）
      use-registered-suffix-pattern: false
    # 内容协商配置（防二次后缀污染）
    contentnegotiation:
      # 禁用路径后缀作为内容协商依据（比如 /export.json）
      favor-path-extension: false
      # 禁用参数作为内容协商依据（比如 /export?format=json）
      favor-parameter: false
      # 仅通过 Accept 请求头判断返回格式（最安全）
      ignore-accept-header: false
  # 禁用静态资源映射（避免 TongWeb 把 /export 误判为静态文件）
  web:
    resources:
      add-mappings: false
```