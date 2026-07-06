
ha高可用模式，不同组件模块有冷备、热备、双活或多活三种模式

|实现方式     |节点个数     |应用状态     |节点切换     |
| --- | --- | --- | --- |
|冷备     | 2    | 主节点正常启动并提供服务，备节点停止    |当主节点发生故障时，通过故障转移机制启动备节点并继续提供服务|
|热备     | 2    | 主节点备节点都启动，但只有主节点提供服务    |当主节点发生故障时，备节点开始提供服务 |
|双活或多活     | >=2    | 每个节点都正常启动并提供服务    |当某个节点发生故障时，其余节点可以承担该故障节点的业务 |

三方组件有HA搭建模式，直接借用即可。

| **本脑模块**|- **高可用方式**|- **节点数目**|
|---|---|---|
| 展示层服务(webserver)| 双活| 2|
| 后台服务(tomcat)| 热备,双活都有| 2|
| 情报匹配(shuri)| 多活| 2个或以上|
| 智能分析工作节(sae-core)| 多活| 2个或以上|
| es查询代理(elasticsearch-proxy)| 双活| 2|
| 脚本执行引擎(script-engine)| 双活| 2|
| 云端反馈(boost)| 双活| 2|
| 采集器工作节点(dv_worker)| 双活| 2个或以上|
| hqlite+查询(hqlite+)| 双活| 2|
| 系统监控(monitor)| 双活| 2|
| ha管理节点(ha-agent)| 热备| 2|
| 批处理分析引擎(angler)| 冷备| 2|
| 采集器控制节点(dv_master)| 冷备| 2|
| 安全事件分析引擎(incident)| 冷备| 2|
| 辅助模块(misc)| 冷备| 2|
| 响应预案(soar)| 冷备| 2|
| 安全实体画像(artifact)| 多活| 2|

tomcat HA相关文档: [Tomcat双活方案设计 | 知识中心](https://geelib.qihoo.net/geelib/knowledge/doc?spaceId=1384&docId=39915)

hqlite只有1个？
dv_master两个分组？
monitor?
csrc? 1个节点
script-engine?
dv-worker?


### HA冷备服务切换逻辑重构
Supervisor监控的进程状态分类：
Available状态：RUNNING 
Unavailable状态：STOPPED、EXITED 
Fault状态：FATAL、BACKOFF 
Transitional状态：STARTING、STOPPING 
Unknown状态：UNKNOWN

Set<String> SUPERVISOR_AVAILABLE_STATE = Set.of(SUPERVISOR_RUNNING_STATE);  //正常可用状态  
Set<String> SUPERVISOR_UNAVAILABLE_STATE = Set.of(SUPERVISOR_STOPPED_STATE, SUPERVISOR_EXITED_STATE);  //正常不可用状态  
Set<String> SUPERVISOR_FAULT_STATE = Set.of(SUPERVISOR_BACKOFF_STATE, SUPERVISOR_FATAL_STATE);  //异常退出状态  
Set<String> SUPERVISOR_TRANSITIONAL_STATE = Set.of(SUPERVISOR_STARTING_STATE, SUPERVISOR_STOPPING_STATE);  //过渡状态  
Set<String> SUPERVISOR_UNKNOWN_STATE = Set.of(SUPERVISOR_UNKONWN_STATE);  //未知状态

#### 核心原则重申

1. **主节点优先**：任何时候，只要主节点能正常运行（或可恢复），优先保证主节点运行，备节点仅作为兜底。
2. **最小操作原则**：对 Transitional 状态（STARTING/STOPPING）优先等待稳定，避免在状态波动时频繁操作。
3. **Fault 状态特性**：主 / 备节点处于 Fault（FATAL/BACKOFF）时，说明其启动能力存在问题（如配置错误、依赖缺失），优先尝试启动 “非 Fault 节点”。
4. **Unknown 状态保守性**：仅在确认服务完全中断时才尝试启动操作，否则维持现状并加强验证。

#### 服务进程切换逻辑

场景 1：主节点 Available（RUNNING）
- 备节点 Unavailable：正常，维持现状。
- 备节点 Available：停掉备节点（防双活）。
- 备节点 Fault：无需操作（Fault 节点本身无法运行，不会双活）。
- 备节点 Transitional：备节点STARTING，停掉备节点，备节点STOPPING，维持现状。
- 备节点 Unknown：维持现状（主节点正常，无需冒险操作备节点）。

场景 2：主节点 Unavailable（STOPPED/EXITED）
- 备节点 Available：正常（主节点故障，备节点接管），维持现状。
- 备节点 Unavailable：优先启动主节点（主节点优先）。
- 备节点 Fault：直接启动主节点（备节点本身启动有问题，优先恢复主节点）。
- 备节点 Transitional：如果备节点stopping，则主动启动主节点，如果备节点starting，则维持现状
- 备节点 Unknown：主节点明确可恢复，执行主节点启动操作。

场景 3：主节点 Fault（FATAL/BACKOFF）
**期望状态**：主节点保持 Unavailable（放弃恢复），备节点变为 Available。
- 备节点 Available：状态符合期望，**不操作**。
- 备节点 Unavailable：**执行备节点启动操作**（主节点无法恢复，启动备节点）。
- 备节点 Fault：主备均无法启动，尝试启动主节点，停掉备节点。
- 备节点 Transitional：如果备节点stopping，**执行备节点启动操作**，如果备节点starting，则维持现状
- 备节点 Unknown：**执行备节点启动操作**（主节点明确故障，备节点无论状态均尝试启动）。维持现状？？？

场景 4：主节点 Transitional（STARTING/STOPPING）
4.1 主节点为 STARTING
- 备节点 Available：状态不符（主节点可能即将可用），**执行备节点停止操作**。
- 备节点 Unavailable：状态符合期望（主节点可能即将恢复），**不操作**。
- 备节点 Fault：状态符合期望（备节点未运行），**不操作**。
- 备节点 Transitional：如果备节点starting，则停掉备节点。
- 备节点 Unknown：**不操作**（主节点状态未明确，避免干扰）。
4.2 主节点为 STOPPING
- 备节点 Available：维持现状（备节点已运行，主节点停止后正常接管）。
- 备节点 Unavailable：启动备节点（防止主节点停止后服务中断）。
- 备节点 Fault：尝试启动备节点。
- 备节点 Transitional：如果备节点starting，则维持现状，如果备节点stopping，则启动备节点。
- 备节点 Unknown：**不操作**（主节点状态未明确，避免干扰）。

 场景 5：主节点 Unknown
**期望状态**：保守保证服务可用（允许主 / 备任一 Available，但避免双活）。
- 备节点 Available：状态符合期望（服务可用），**不操作**。
- 备节点 Unavailable：**执行主节点启动操作**（优先尝试恢复主节点）。
- 备节点 Fault：**执行主节点启动操作**（尝试恢复主节点，备节点不可用）。
- 备节点 Transitional：
    - `STARTING`：可能变为 Available，**不操作**（等待其稳定）。
    - `STOPPING`：即将变为 Unavailable，**执行主节点启动操作**。
- 备节点 Unknown：**不操作**（避免双活风险，下周期再校验）。