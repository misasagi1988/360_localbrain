# 本脑SAE规则衍进

标签（空格分隔）： SAE_DOC

---

# 本脑1.0版本

本脑1.0版本sae规则有规则类型，场景类型划分没有很详细。

# 本脑1.5版本

本脑1.5版本对应sim1.5版本。sae规则不再有规则类型，更新为信息模型。规则使用字段说明如下：

- 过滤条件和关联条件使用的是事件对应模型的所有必选及可选字段+多维度关联分析的所有字段(威胁情报、资产+脆弱性)；
- 分组字段、distinct字段、sum字段使用的是事件对应模型的所有必选及可选字段；
- 输出结果里强制输出信息模型里的必选字段，可以选择输出事件对应模型的所有必选及可选字段，标记属性的话使用的是所有告警及日志的字段。

# 本脑2.0版本

本脑1.5版本对应sim2.0版本。引入了实体的概念：

- 过滤条件、关联条件都是使用的是该事件在解析规则中被解析出的字段+多维度关联分析的所有字段(威胁情报、资产+脆弱性)；
- 分组字段、distinct字段、sum字段都是使用的是该事件在解析规则中被解析出的字段；
- 如果规则中配置了实体，输出结果里推荐输出事件被解析出的字段与实体的核心字段的交集，可以选择输出事件被解析出的其他字段，标记属性的话使用的是所有告警及日志的字段。

参考文档：http://wiki.b.qihoo.net/pages/viewpage.action?pageId=22696797



# 全局白名单过滤字段
    public static final String SRC_ADDRESS_FIELD = "src_address"; //src address
    public static final String DST_ADDRESS_FIELD = "dst_address"; //dst address
    public static final String DOMAIN_FIELD = "domain_name"; //domain
    public static final String URL_FIELD = "http_url_path"; //url  URL
    public static final String USER_NAME_FIELD = "user_name"; // user account   用户名称


