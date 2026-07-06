# 一体机artifact clickhouse改造

标签（空格分隔）： CK

---

### 改造过程中存在的问题调研

<font color="red" size="5">**aggregation table**</font>

不涉及改动，表引擎选择mergeEngine即可。
表结构设计问题：在不同的聚合关系里，部分属性字段的类型不一致，如dst_port，有些是long，有些是String[]。字段及类型定义暂定：

<u>***必备字段***</u>
win_start      long
win_end      long
agg_id      keyword
agg_count      long
group_key      keyword
occur_time      Object, firstTime/lastTime

<u>***可选extract字段***</u>
md5 String                                  keyword
client_host_sign String                     keyword
name String[]                               keyword
host_ip String/String[]                     keyword
domain_name String                          keyword
dst_address String/String[]                          keyword
event_name String/String[]                          keyword
src_address String/String[]                          keyword
dst_port long/String[]                          keyword
protocol String[]                          keyword
user_name String                          keyword
host_name String[]                          keyword

目前暂不确定其对查询的影响。

<font color="red"  size="5">**entity table**</font>

实体表采用ck存储存在的问题：
- 鉴于实体需定期频繁更新，更新频率很高，需评估改用ck存储是否合理。
- 实体的更新采用的是增量更新方式，利用es的脚本实现的，如果换为ck，增量更新逻辑是否需要改动，如果改为全量更新，会加大内存占用。

调研了下ClickHouse更新数据的方法，建议采用ReplacingMergeTree的方式。AggregatingMergeTree使用SimpleAggregateFunction还算ok，用anyLast也可以，但查询时需要带FINAL；而使用普通的AggregateFunction做聚合查询比较麻烦，不符合我们的需求，而且聚合函数不满足我们的场景需要，增量更新的方式无法实现。如果采用ReplacingMergeTree，或AggregatingMergeTree+SimpleAggregateFunction，更新方式需改为全量更新。

### 实现思路
aggregation table，所有聚合关系共用一个表，表语句demo:
```sql
CREATE TABLE soc.artifact_aggregation
(
    win_start DateTime64(3, 'Asia/Shanghai'),
    win_end DateTime64(3, 'Asia/Shanghai'),
    agg_id String,
    agg_count UInt64,
    group_key String,
    source String
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(win_start)
ORDER BY agg_id
```
entity table，不同entity采用不同的表结构，表引擎使用ReplacingMergeTree，表语句demo:
```sql
CREATE TABLE soc.artifact_entity_intranet_machine
(
    machine_id String,
    binding_ip String,
    first_seen_time UInt64,
    last_update_time UInt64,
    timestamp UInt64,
    host_name Array(String),
    ip String
    ...
)
ENGINE = ReplacingMergeTree(timestamp)
ORDER BY machine_id
```

### ClickHouse更新数据方法调研

参考：https://zhuanlan.zhihu.com/p/485645089

ck提供了好几种MergeTree表引擎，可以通过以增代删的思路，实现行级数据修改和删除。下面有几种方法就是利用这种思路来实现的。调研的几种更新思路如下：

- Partition Operations: 大致思路是操作分区，有更新就删掉原分区，用新的分区替代。分区交换对于低频率的批量数据更新比较有用，但当需要实时高频率的更新数据时，它们就不那么方便了。此外，开发人员操作分区还是不太方便的，因此这种方法一般用的比较少。
- Update方法: ck的更新操作是一个异步的操作。
当用户执行一个update操作获得返回时，ck其实只做了两件事情：1.检查update操作是否合法；2.保存update命令到存储文件中，唤醒一个异步处理merge和mutation的工作线程。异步线程的工作流程极其复杂，其精髓在于，先查找到需要update的数据所在datapart，之后对整个datapart做扫描，更新需要变更的数据，然后再将数据重新落盘生成新的datapart，最后用新的datapart做替代并remove掉过期的datapart。这就是ck对update指令的执行过程，可以看出，频繁的update指令对于ck来说将是灾难性的。
- Incremental Log: clickhouse的两种表引擎，CollapsingMergeTree、VersionedCollapsingMergeTree支持通过合并实现数据更新。但这两个表引擎在插入数据时都要求记录数据的原状态，在更新数据时，先插入一笔原数据对应的“cancel” 行，同时插入一笔更新数据，以实现合并时的数据更新。CollapsingMergeTree对于写入数据的顺序有着严格要求，否则导致无法正常折叠。这种方式，一是要保留更新前的原数据，二是会造成写放大，而且查询也不方便。
- Insert+xxxMergeTree: 用Insert加特定引擎，也可以实现更新效果。该方法适用于xxxMergeTree，如ReplacingMergeTree或AggregatingMergeTree。但更新是异步的。因此刚插入的数据，并不能马上看到最新的结果，因此并不是准实时的。需手动下发optimize指令强制聚合过程的执行。demo: https://developer.aliyun.com/article/781084
- Insert+xxxMergeTree+Final: 仍使用上述方案，但在查询时，加入final关键字。但这个查询时一个串行过程，会做分区合并，代价比较高，也不宜频繁使用。
- Insert+argMax: 这种思路主要使用 ReplacingMergeTree表引擎，在查询时使用函数argMax(field1，field2)，根据field2 的最大值取 field1 的值，得到最新的结果。demo: https://cloud.tencent.com/developer/article/1644570
- OPTIMIZE FINAL: 可以进行强制刷新(OPTIMIZE TABLE {tableName} FINAL)，但OPTIMIZE操作速度慢，代价高，因此不能频繁的执行。

总结：

| 方法 | 实时性 | 优点 | 不足 | 适合场景 |
| :-----| :---- | :---- | :---- | :---- |
| Partition Operations | 非准实时 |  | 不适用于实时场景；操作不便 |大批量修改，非准实时场景 |
| Update | 非准实时 |  | 异步操作，代价很大，不能频繁使用 | |
| Incremental Log | 可以通过优化查询语句实现准实时 | 某些场景可以用这个办法取巧解决 | 要先保留原数据；某些计算场景并不适合，比如min、max等其他场景 |对于sum、count、avg等非unique场景 |
| Insert+xxxMergeTree | 非准实时 |  | 最终一致性；不适用于实时场景 |对实时性要求不高的场景 |
| Insert+xxxMergeTree+Final | 准实时 | 准实时 | Final不能频繁使用 |如果查询不频繁，可以用这个来实现准实时 |
| Insert+argMax | 准实时 | 实时性好，开销相对能接受 | 查询语句较为复杂；内存开销较大 |适用于修改较频繁的场景 |
| OPTIMIZE FINAL | 准实时 | 操作后，一定是最新的 | 代价很大，耗时很长，不可频繁使用 |某些验证场景，或者临时操作 |


