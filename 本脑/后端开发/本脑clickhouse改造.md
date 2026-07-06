标签（空格分隔）： 本脑v4.5版本

---
### 需求说明

本脑4.5版本，Elasticsearch和Clickhouse兼容
通过mysql配置判断是否为Clickhouse版本:
```sql
INSERT INTO system_config (id, type, config, createor_id, updator_id, create_time, update_time) VALUES ('0FRM65EVYAA1', 'clickhouse_enable', true, 'FIKVIZS30007','FIKVIZS30007','2024-06-19 17:18:45','2024-06-19 17:18:45')
```
试验: 挑选部分客户，event不再存储在es，改为clickhouse。

### 设计

dv将数据写入hes-store-group-0，交由transfer模块转储到clickhouse。
Clickhouse存储event数据。Elasticsearch存储除event外所有数据。
所有event数据存储在同一个表中。通过日期及数据源进行分区，同时兼容存储策略。结构类似，数据压缩比更高。
暂不支持HA。

### clickhouse event数据表设计

新建event数据表，所有日志写入一个该数据表
  - _source存储完整日志（包含解析后的字段和原始数据）
  - 通过JSON_EXTRACT抽取常用字段，依赖simdjson高性能json抽取处理（抽取80个字段占用5核左右，相比抽取10个字段占用1核左右）
  - 依据 storage_config 以及 日期进行分区
  - 使用MergeTree引擎
  - 分区配置：PARTITION BY (toYYYYMMDD(occur_time), storage_cfg)，其中，storage_cfg由数据源值 + "_" + 存储策略ID组成，如果不匹配任何存储策略，则存储策略ID为空，如果数据源值为null，则数据源值为空。

### misc模块改造

#### 存储策略相关，数据过期检测与删除

每天定时调用misc相关函数：
1. 通过查询system.parts表获取event索引的partition
2. 分析partition，按存储策略ID分组
3. 获取存储策略ID相关的存储策略指定的数据期望保存天数，利用strategy_id做filter条件，根据system.parts表的min_time(该字段保存了相关partition的最小日志时间)，获取该存储策略关联的过期partition后删除
4. 过期删除后，将backup_event数据表的原partition数据restore到event(告警溯源日志还原)，strategy_id设置为backup，这种partition不删除。

#### 磁盘空间保护

只清理日志数据。每天定时调用misc相关函数：
1. 通过查询system.disks表获取clickhouse磁盘空间使用情况
2. 如果超过清除阈值，则从最老的数据开始，按天删除分区，清除分区时，优先删除不匹配任何存储策略的数据，再清理匹配存储策略的数据，每清理完一天的数据，则check磁盘空间使用率，仍然超过清除阈值，则继续清理，直到磁盘空间使用率低于清除阈值或者所有数据的时间都在期望存储范围之内为止
3. 如果超过告警阈值，则警告
4. 清除partition后，将backup_event数据表的原partition数据restore到event(告警溯源日志还原)，strategy_id设置为backup，这种partition不删除。

#### 告警溯源日志备份

每天定时调用misc相关函数：
1. 将1天分成24个小时，根据range query查询es，获取startTime在那些个时间范围内的告警，获取告警的溯源日志id字段event_id，去重
2. 使用`INSERT INTO backup_event SELECT ...`，过滤出触发告警的event数据表的日志数据，备份至backup_event数据表
3. clickhouse  in子句理论上可以支持很多个值，但具体的数量并没有一个固定的明确上限，如果值过多，会导致性能下降，内存消耗也增加，这里采用分批索引的方式，每个批次包含1000个值








