
---
升级背景：
现在在使用nacos-server 2.4.2做模块配置管理与服务发现，因为CVE-2024-38816，CVE-2024-38819这两个漏洞的原因，需要升级nacos-server版本
环境各模块nacos相关依赖情况：
springboot版本: 3.5.14
com.alibaba.boot:nacos-config-spring-boot-starter:0.3.0-RC
com.alibaba.boot:nacos-discovery-spring-boot-starter:0.3.0-RC
com.alibaba.nacos:nacos-client:2.3.2
com.alibaba.nacos:nacos-spring-context:2.1

## 一、推荐版本：Nacos Server 3.2.1

### 1.1 版本概览

|版本|发布日期|状态|Spring Boot 版本|Java 要求|
|---|---|---|---|---|
|3.0.x|2025-Q3|早期稳定版|3.4.x|JDK 17|
|3.1.0-BETA|2025-Q4|测试版|3.4.x|JDK 17|
|3.1.1|2025-11-26|稳定版|3.4.9|JDK 17|
|3.2.0|2026-03-27|稳定版|3.4.10|JDK 17|
|**3.2.1**|**2026-04**|**最新稳定版**|**3.5.13**|**JDK 17**|
|3.2.1-2026.04.03|2026-04-03|补丁版|3.5.13|JDK 17|

### 1.2 为什么选择 3.2.1 而非 3.0.x 或 3.1.x？

|维度|3.0.x|3.1.1|**3.2.1**|
|---|---|---|---|
|Spring 框架 CVE 修复|基础修复|修复至 3.4.9|修复至 3.5.13，含 CVE-2025-55752 及全部 Spring 6.2.x 安全修复|
|插件体系|基础|基础|**完整 SPI 插件发现与管理**|
|DB 密码加密插件|需手动集成|需手动集成|**nacos-db-password-encryption-plugin 官方支持**|
|国产数据库插件|社区维护|社区维护|**官方 nacos-plugin 仓库统一维护**|
|安全性|中等|较高|**最高**|
|Bug 修复覆盖|有限|较多|**最全**|
|社区活跃度|过渡期|活跃|**最活跃**|

## 二、CVE 漏洞修复依据

### 2.1 漏洞本质

CVE-2024-38816 和 CVE-2024-38819 是 **Spring Framework** 层面的路径遍历漏洞（Path Traversal），影响 `spring-webmvc` 和 `spring-webflux` 的功能式 Web 框架（WebMvc.fn / WebFlux.fn）：

|CVE 编号|CVSS 评分|漏洞类型|修复版本（Spring Framework）|
|---|---|---|---|
|CVE-2024-38816|7.5 (High)|CWE-22 路径遍历|6.1.13+ / 6.0.24+ / 5.3.40+|
|CVE-2024-38819|7.5 (High)|CWE-22 双重 URL 编码路径遍历|6.1.14+ / 6.0.25+ / 5.3.41+|

### 2.2 Nacos 2.4.2 的风险

Nacos Server 2.4.2 内嵌的 Spring Framework 版本 **低于上述修复版本**，其 `spring-webmvc` 组件存在路径遍历漏洞。攻击者可通过构造恶意 HTTP 请求（如 `/%2E%2E/../../../../etc/passwd` 或双重 URL 编码 `%252E%252F`）绕过路径校验，读取服务器任意文件。

### 2.3 Nacos 3.2.1 的修复路径

Nacos 3.x 全面升级了底层依赖链：
Nacos 2.4.2:  
  └── Spring Boot 2.x / Spring Framework 5.x ──→ 存在 CVE-2024-38816/38819  
​  
Nacos 3.2.1:  
  └── Spring Boot 3.5.13  
       └── Spring Framework 6.2.x ──→ 已修复 CVE-2024-38816/38819  
       └── 同时修复 CVE-2025-55752（Spring Boot 相关漏洞）

Nacos 3.2.1 进一步将 Spring Boot 从 3.4.10 升级到 **3.5.13**。

## 三、客户端依赖兼容性（总览）

**升级 Nacos Server 本身不需要升级任何客户端依赖**。以下是各依赖的详细分析：

|依赖|当前版本|能否保持不升|已知问题|
|---|---|---|---|
|`com.alibaba.boot:nacos-config-spring-boot-starter`|0.3.0-RC|可保持|与 Spring Boot 3.5.14 存在 SnakeYAML 2 依赖冲突风险|
|`com.alibaba.boot:nacos-discovery-spring-boot-starter`|0.3.0-RC|可保持|与 Spring Boot 3.5.14 存在 SnakeYAML 2 依赖冲突风险|
|`com.alibaba.nacos:nacos-client`|2.3.2|可保持|gRPC 连接稳定性有若干 bug 已在后续版本修复，不升级配置自动更新可能有问题，nacos日志中一直有这个WARN No mapping for POST /nacos/v1/cs/configs/listener|
|`com.alibaba.nacos:nacos-spring-context`|2.1.0|可保持|支持 Spring 6，无已知阻断问题|

## 四、四款数据库支持方案

### 官方 + 插件支持矩阵

Nacos 3.2.1 结合官方 `nacos-plugin` 项目可支持当前所需的全部四种国产数据库：

|数据库|插件名称|仓库路径|支持状态|
|---|---|---|---|
|**PostgreSQL**|`nacos-postgresql-datasource-plugin-ext`|nacos-group/nacos-plugin|官方维护（已合并至主仓库）|
|**DM8（达梦）**|`nacos-dm-datasource-plugin-ext`|nacos-group/nacos-plugin|已支持|
|**Kingbase8（人大金仓）**|`nacos-kingbase-datasource-plugin-ext`|nacos-group/nacos-plugin|已支持|
|**OceanBase**|`nacos-oceanbase-datasource-plugin-ext`|nacos-group/nacos-plugin|已支持|

### 四种数据库关键差异对比

|项目|DM8|KingbaseES V8|PostgreSQL|OceanBase|
|---|---|---|---|---|
|平台标识|`dm`|`kingbase`|`postgresql`|`oceanbase`|
|JDBC 驱动类|`dm.jdbc.driver.DmDriver`|`com.kingbase8.Driver`|`org.postgresql.Driver`|`com.oceanbase.jdbc.Driver`|
|空字符串 = NULL|否（Oracle 兼容模式下部分场景是）|**是**（需修改配置关闭）|否|MySQL 租户：否；Oracle 租户：**是**|
|分页语法|`LIMIT ... OFFSET`|`LIMIT ... OFFSET`|`OFFSET ... LIMIT`|取决于租户模式|
|推荐兼容模式|Oracle 兼容模式|Oracle 兼容模式|原生模式|MySQL 租户模式|
|默认端口|5236|54321|5432|2883（代理）/ 2881（直连）|

## 五、密码加密连接方案

nacos插件仓库`nacos-group/nacos-plugin` 项目提供了 **`nacos-db-password-encryption-plugin`**，位于：

nacos-custom-environment-plugin-ext/  
  └── nacos-db-password-encryption-plugin/

该插件通过 SPI 机制，允许在 `conf/application.properties` 中配置加密的 `db.password.0`，Nacos Server 启动时自动解密后建立数据库连接。

## 六、数据库升级

schema变动，增加部分数据表，部分数据表schema有变动，但无需做数据迁移。


## 七、参考链接

|资源|URL|
|---|---|
|官方下载|[https://nacos.io/en/download/release-history](https://nacos.io/en/download/release-history)|
|升级指南|[https://nacos.io/en/docs/latest/manual/admin/upgrading](https://nacos.io/en/docs/latest/manual/admin/upgrading)|
|数据源插件文档|[https://nacos.io/en/docs/latest/plugin/datasource-plugin](https://nacos.io/en/docs/latest/plugin/datasource-plugin)|
|GitHub Releases|[https://github.com/alibaba/nacos/releases](https://github.com/alibaba/nacos/releases)|
|官方插件仓库|[https://github.com/nacos-group/nacos-plugin](https://github.com/nacos-group/nacos-plugin)|

## 注意点

之前因为nacos-spring-context模块依赖的snakeyaml版本太低，存在CVE漏洞，客户强制要求将snakeyaml版本升级到2版本，本脑为了适配，对nacos-spring-context模块做了定制改造，后面升级时要注意这个问题，看升级后的版本snakeyaml对应的版本是否ok。起码目前，nacos-spring-context 2.1.1依赖的snakeyaml版本还是很低，snakeyaml为1.29版本，存在漏洞，需做适配。

## 升级问题
1. webserver启动失败，前端的说法是目前的sdk不支持nacos-3

2. nacos.log 接口报warning: No mapping for GET /nacos/v1/cs/configs，不确定是哪个模块做的请求，猜测是message-bus，相关代码：configService.getConfig("base.yml", "DEFAULT_GROUP", 300000L)
这个问题已通过使用接口API适配插件来解决，该插件可以将v1/v2 的 HTTP 接口重新挂载到 Nacos Server 上，让旧版本的
  client（或仍走 v1 路径的 starter）能正常调用。这样webserver也就无需改动了。nacos-client也不需要升级了。
  
3. nacos服务发现问题，需升级nacos-client版本
```
2026-06-01 14:58:32,832 ERROR CONSOLE /metrics

org.springframework.web.servlet.resource.NoResourceFoundException: No static resource metrics.
        at org.springframework.web.servlet.resource.ResourceHttpRequestHandler.handleRequest(ResourceHttpRequestHandler.java:585)
        at org.springframework.web.servlet.mvc.HttpRequestHandlerAdapter.handle(HttpRequestHandlerAdapter.java:52)
        at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1089)
        at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:979)
        at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1014)
        at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:903)
        at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:564)
        at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:885)
        at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:658)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:51)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:162)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at com.alibaba.nacos.console.filter.XssFilter.doFilterInternal(XssFilter.java:42)
        at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:162)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:91)
        at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:162)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at com.alibaba.nacos.core.paramcheck.ParamCheckerFilter.doFilter(ParamCheckerFilter.java:71)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:162)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at com.alibaba.nacos.core.auth.AbstractWebAuthFilter.doFilter(AbstractWebAuthFilter.java:76)
        at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:162)
        at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:138)
        at org.springframework.web.filter.CompositeFilter$VirtualFilterChain.doFilter(CompositeFilter.java:108)
        at org.springframework.security.web.FilterChainProxy.lambda$doFilterInternal$3(FilterChainProxy.java:231)
        at org.springframework.security.web.ObservationFilterChainDecorator$FilterObservation$SimpleFilterObservation.lambda$wrap$1(ObservationFilterChainDecorator.java:490)
        at org.springframework.security.web.ObservationFilterChainDecorator$AroundFilterObservation$SimpleAroundFilterObservation.lambda$wrap$1(ObservationFilterChainDecorator.java:351)
        at org.springframework.security.web.ObservationFilterChainDecorator.lambda$wrapSecured$0(ObservationFilterChainDecorator.java:83)
        at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:129)
        at org.springframework.security.web.access.intercept.AuthorizationFilter.doFilter(AuthorizationFilter.java:101)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:241)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:228)
        at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:138)
        at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:125)
        at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:119)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:241)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:228)
        at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:138)
        at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:100)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:241)
        at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:228)
        at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:138)
        at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:179)
```