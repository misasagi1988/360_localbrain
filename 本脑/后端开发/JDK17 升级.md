标签（空格分隔）： 本脑v4.0版本

---

### no need

我们使用的tomcat为9版本，支持jdk17，它使用的Servlet版本为4，依赖的还是javax相关的
springboot为2.7版本，使用的依赖也是javax相关的。
后面如果要升级springboot版本到3，tomcat需升级至10，javax相关依赖需切换至jakatar.

### 改造需知

1. 模块化导出
从JDK 9 开始引入的模块系统对 Java 平台的内部 API 访问进行了严格的控制，它旨在提供更强的封装性和更清晰的依赖关系，减少不同组件间的耦合。在模块化的世界中，许多 JDK 的内部 API（如 `sun.*` 和 `jdk.internal.*` 包中的类）不再是公开的，因此无法直接从应用程序代码中访问。
为了允许模块化后的 JDK 中的某些内部 API 被访问，可以使用 `--add-exports` 参数在编译及JVM 启动时放宽模块的导出限制。例如，`--add-exports java.base/sun.net.util=ALL-UNNAMED` 允许未命名模块（即没有模块描述符的模块）访问 `java.base` 模块中的 `sun.net.util` 包。
在可能的情况下，建议修改代码，寻找官方支持的替代方案来代替 JDK 内部 API。
demo:
```
gradle: 
tasks.withType(JavaCompile).configureEach { 
    options.compilerArgs.addAll([  
            "--add-exports", "java.base/sun.net.util=ALL-UNNAMED"
            ])
}

JVM启动参数: --add-opens java.base/sun.net.util=ALL-UNNAMED
```

2. gradle版本升级
gradle需升级至7以上版本
在 Gradle 7 中，`compile` 配置已经被弃用，取而代之的是 `implementation` 和 `api` 配置。

3. JVM启动参数改造
使用模块化导出，控制JDK内部模块的可见性；
gc相关参数改动，原有的`UseGCLogFileRotation`相关参数已不再支持，需适配改造：
```
jdk8:
  -XX:+UseGCLogFileRotation \
  -XX:NumberOfGCLogFiles=5 \
  -XX:GCLogFileSize=10M \
  -Xloggc:/opt/qihoo/soc/tomcat/logs/gc/gc-%t.log \
  -verbose:gc \

jdk17:
  -Xlog:gc*=info:file=/opt/qihoo/soc/tomcat/logs/gc/gc.log-%t:level,tags,time,uptime,pid:filecount=5,filesize=10M \
  -verbose:gc \
```


### 待改造模块

f-jdk17-adaptor

| module | owner | status |
| --- | --- | --- |
| angler |     | done |
| artifact |     | done |
| boost/feedback |     | done |
| ha-agent |     | done |
| dv |   | done |
| hqlite-plus | 刘如浩 | done |
| incident |     | done |
| nacos |     | done |
| misc |     | done |
| monitor |     | done |
| sae-core |     | done |
| shuri |     | done |
| skywalking |     | done |
| soar | 李刚  | done  |
| script-engine | 李刚 | done |
| tomcat |     | done |
| tomcat-sae |     | done |
| tomcat-ice |     | done |
| atom_install |     | done |
| dependency related |     |     |

