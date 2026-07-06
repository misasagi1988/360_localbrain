# SOAR

标签（空格分隔）： 360BrainSecurity

---

SOAR: 是Security Orchestration, Automation and Response，即安全编排和自动化响应
根据Gartner2019年最新定义，SOAR是指能使企业组织从SIEM等监控系统中收集报警信息，或通过与其它技术的集成和自动化协调，提供包括安全事件响应和威胁情报等功能。SOAR技术市场最终目标是将安全编排和自动化(SOA)、安全事件响应(SIR)和威胁情报平台(TIP)功能融合到单个解决方案中。


## 相关概念
- 应用联动：联动的三方应用，提供操作动作，供自动化脚本使用
- 预案: 组合一系列自动化动作，完成一个任务，预案支持嵌套，自动、人工。预案的入参除了自动化支持的几种类型外，增加了“告警”和“安全事件”类型。预案使用的自动化动作如果用到了应用，需要绑定应用实例。
- 自动化：自动化python脚本，实现单一的功能，可理解为一个函数，有入参出参，可调用特定应用联动的接口实现操作

## 数据表
soar_automation ##自动化
soar_playbook ##预案
soar_integration_plugin ##应用联动
soar_integration_plugin_command ##应用提供的命令
soar_integration_instance ##应用实例信息

## 应用场景
sae规则、ice规则、定时触发、智能分析、仪表盘、安全事件、资产管理、实体画像，预案页面手动触发

## 运行环境
docker，支持python2，python3

## 应用联动内容包
应用联动内容包的文件格式需遵循一定格式：
libs: 存放本应用所依赖的Python库
plugin.ico: 在页面展示的应用的LOGO信息；
plugin.py: 应用联动主体脚本内容，会展示在页面上；
plugin.yml: 定义本应用的各个函数，函数的入参（类型、是否必选、参数说明等）。

应用联动验证：导入应用联动，配置自动化，添加预案，执行预案。




