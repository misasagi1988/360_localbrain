标签（空格分隔）： 本脑v4.5版本

---

### tomcat 本地配置文件整理

```
config/announce/properties/config.properties，普通配置文件
config/asset/score.properties，该文件是整个加载的供资产打分用的，不建议放到nacos上分key读取使用，参考AssetEntryPoint
config/attack/properties/config.properties，普通配置文件
config/common/properties/config.properties，普通配置文件
config/custom/properties/cronConfig.properties，这三个配置都是人行上报功能及IP/Domain信誉库功能相关，建议优化相关代码，相关配置可移至nacos，由springboot加载
config/custom/properties/push.properties
config/custom/properties/timer.properties
config/discover/properties/config.properties，普通配置文件
config/event/properties/colshow.properties，搜索没有用到的地方，猜测已废弃
config/global_trend/properties/config.properties，普通配置文件
config/gpt/properties/config.properties，普通配置文件
config/notification/properties/config.properties，普通配置文件
config/report/properties/config.properties，普通配置文件
config/secinfo/properties/config.properties，普通配置文件
config/secinfo/properties/score.properties，该文件是是整个加载的供风险评估用的，不建议放到nacos上分key读取使用，参考
config/security_device/properties/config.properties，普通配置文件
config/system/properties/config.properties，配置文件，但有接口调用改动install.dir的值，需要进一步改造
config/system/properties/space_usage.properties，搜索没有用到的地方，猜测已废弃
config/work_order/properties/config.properties，普通配置文件
```

| 模块 | 配置文件 | 功能 | HA模式影响 |
| --- | --- | --- |
| announce | properties/config.properties | no |
| asset | score.properties | no |
| attack | properties/config.properties | no |
| common | properties/config.properties | yes, ha运行模式相关配置 |
| custom | properties/cronConfig.properties,properties/push.properties,properties/timer.properties | 不太确定这几个配置文件干嘛用的 |
| discover | properties/config.properties | no |
| event | properties/colshow.properties | no |
| global_trend | properties/config.properties | no |
| gpt | properties/config.properties | no |
| notification | properties/config.properties | no |
| report | properties/config.properties,非键值对格式，奇怪 | no |
| secinfo | properties/config.properties,properties/score.properties | no |
| security_device | properties/config.properties | no |
| system | properties/config.properties,properties/space_usage.properties | yes |
| work_order | properties/config.properties | no |

当前tomcat环境中，加载配置的功能主要是在GlobalUtils类中实现的，有很多类(包括工具类、常量类)都使用了该工具类提供的方法，获取配置字段的值。
它的主要实现逻辑是，在初次调用时，读取classpath:config目录下的所有config.properties文件，将键值对加载到map中，调用时直接返回map的相关key的值。

### 迁移方案设计

1. 使用nacos config Spring Boot多配置文件支持功能实现迁移，将所有配置文件放到tomcat application.yml的nacos配置项中引用。
一开始的思路是采用这种方式，但实验下来，这种方式并不合理：
可能与目前配置文件的key有重复，导致覆盖；
我们只能通过springboot applicationContext的Environment bean对象，调用其getProperty()方法获取键值。但该类是一个工具类，工具方法也都是static的，无法自动注入Environment bean。applicationContext为null，无法使用工具类getBean；
该类无法转成bean，有太多地方引用该类，尤其是一些工具类和常量类，转成bean不合理。
2. 将所有配置文件信息(data-id,group,namespace)放入本地application.yml，但不通过nacos引入，tomcat启动时读取application.yml，获取nacos server配置，通过nacos API获取各个配置文件的内容，转键值对后存入map。
该方案主要工作流与原有实现逻辑类似，只是内容由从文件读，改为从nacos上获取，改动不大。
最终决定使用该方案。

feature分支：f-4.5-config-to-nacos
改动涉及模块：
atom_service
atom_install
database-mgr

### 本脑不同部署模式受影响的配置文件

1. system配置
  - 多级部署方式: system.node.deploy.type
  - 本地节点IP:  system.config.node.ip
2. common配置
  - 广播消费consumer: common.messagebus.boardcast.consumer.groupid
  - HA模式相关:  common.tomcat.ha.mode, common.tomcat.ha.status

### Nacos  Config Spring Boot多配置文件支持

可以使用nacos扩展配置项`nacos.config.ext-config`引用多个配置文件，ext-config[index] 的优先级，index越小，优先级越高，从0开始

demo:
```
nacos:
  config:
    server-addr: 127.0.0.1:8848
    username: admin # Nacos鉴权
    password: Q!hooS0c
    bootstrap:
      enable: true
    data-ids: base.yml,main.yml # 主配置
    type: YAML
    group: DEFAULT_GROUP
    auto-refresh: true
    ext-config: # 扩展配置，包含更多选项
      - data-id: config1 # 扩展配置文件1的Data ID
        type: PROPERTIES # 扩展配置文件1的文件类型
        group: DEFAULT_GROUP # 扩展配置文件1的分组
        auto-refresh: true
      - data-id: config2 # 扩展配置文件2的Data ID
        type: PROPERTIES # 扩展配置文件2的文件类型
        group: DEFAULT_GROUP # 扩展配置文件2的分组
        auto-refresh: true
```




### Spring Boot项目配置文件加载过程

Spring Boot 使用两种主要的配置文件格式：`application.properties`(键值对方式) 和 `application.yml`(YAML格式)。这些配置文件用于定义应用程序的配置属性，它们可以被 Spring 环境抽象层读取并用于配置应用程序的行为。

Spring Boot 会在以下位置搜索 `application.properties` 或 `application.yml`：
- 当前目录下的 `/config` 子目录
- 当前目录下的 `/resources` 子目录
- 当前项目的 `classpath` 根路径

当项目目录下存在多个 `application.yml` 配置文件时，Spring Boot 会根据以下规则来选择加载哪些配置文件：
1. **激活的配置文件**：如果你通过 `spring.profiles.active` 指定了激活的配置文件，Spring Boot 会首先加载与激活的配置文件相对应的 `application-{profile}.yml` 或 `application-{profile}.properties` 文件。如果没有找到激活的配置文件，它会回退到加载不带 profile 的 `application.yml` 或 `application.properties`。
2. **配置文件的搜索顺序**：Spring Boot 会按照以下顺序搜索配置文件：
    - `/BOOT-INF/classes`（或 `/WEB-INF/classes` 对于 WAR 文件）
    - `/META-INF/spring` 目录
    - 当前目录下的 `/config` 子目录
    - 当前目录下的 `/resources` 子目录
3. **配置文件的加载**：在搜索到的每个目录中，Spring Boot 会加载以下配置文件：
    - `application.yml` 或 `application.properties`
    - `application-{profile}.yml` 或 `application-{profile}.properties`，其中 `{profile}` 是当前激活的配置文件名
4. **配置文件的合并**：如果存在多个配置文件，Spring Boot 会按照它们在类路径中的顺序进行合并。这意味着，如果一个配置项在多个文件中都出现了，后面加载的文件中的配置项会覆盖前面加载的文件中的相同配置项。
5. **外部配置**：除了上述目录中的配置文件外，Spring Boot 还支持从外部位置（如命令行参数、环境变量等）加载配置。
6. **配置文件的覆盖**：在类路径中的 `application.yml` 会被 `/BOOT-INF/classes/application.yml` 覆盖，如果存在的话。同样，`/config` 目录下的 `application.yml` 也会被 `/resources` 目录下的 `application.yml` 覆盖。
7. **命令行参数**：最后，命令行参数会覆盖所有其他配置源中的配置项。
==**测试来看**==，启动jar包时，首先加载启动目录下的`application.yml`，如果存在config目录，也会加载该目录下的`application.yml`，没有加载resources目录下的。后面的可以引用前面的实现配置属性的继承。

### Spring Boot项目引用配置文件配置字段的方式

1. @ConfigurationProperties：
使用@ConfigurationProperties注解可以创建一个专门的类来绑定配置属性。这个类可以自动加载application.yml中的属性，并可以通过组件扫描（@ComponentScan）被Spring容器管理。
```
@Component
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    // 其他属性和getter/setter...
}
```

2. @Value注解：
@Value注解可以直接注入配置属性的值到字段或方法参数中。
```
@Component
public class SomeComponent {
    @Value("${app.name}")
    private String name;
    // ...
}
```

3. Environment抽象：
通过注入Environment对象，可以编程方式访问配置属性。
与`@ConfigurationProperties`相比，直接使用`Environment`可能牺牲了类型安全，因为返回的属性通常是`String`类型。
```
@Component
public class SomeComponent {
    @Autowired
    private Environment environment;

    public String getName() {
        return environment.getProperty("app.name");
    }
    // ...
}
```

4. @PropertySource注解：
如果你需要从特定的配置文件加载属性，可以使用@PropertySource注解指定配置文件。
```
@Configuration
@PropertySource("classpath:another-config.properties")
public class SomeConfig {
    // ...
}
```

5. @Configuration注解：
在配置类中，可以使用@Configuration注解直接定义配置属性。
```
@Configuration
public class SomeConfig {
    @Bean
    public SomeBean someBean(@Value("${app.name}") String name) {
        return new SomeBean(name);
    }
    // ...
}
```
