# ClickHouse study

标签（空格分隔）： CK

---

参考：https://clickhouse.com/docs/zh

### 一体机artifact clickhouse改造问题
<font color="red">**ck aggregation table**</font>
不涉及改动，mergeEngine即可
表结构设计问题：
部分字段在不同的聚合关系里，属性类型不一致，已知dst_port，有些是long，有些是String[]
必备字段
win_start      long
win_end      long
agg_id      keyword
agg_count      long
group_key      keyword
occur_time      Object, firstTime/lastTime

可选extract字段：
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


<font color="red">**ck entity table**</font>
实体需定期频繁更新，需评估用ck存储是否合理
目前实体的更新采用的是增量更新方式，利用es的脚本实现的
如果换为ck，增量更新逻辑应该需要改动，改为全量更新，这会加大内存占用
ck更新思路：https://zhuanlan.zhihu.com/p/485645089
ck支持数据更新的表引擎：CollapsingMergeTree、VersionedCollapsingMergeTree。这两个表引擎在插入数据时要求记录数据的原状态以取消它，并在更新时插入一笔“cancel” 行，同时插入一笔更新数据。
目前调研的思路：
Insert + AggregatingMergeTree，字段使用SimpleAggregateFunction指明使用的聚合策略(anyLast聚合函数声明聚合策略为保留最后一次的更新数据)，非准实时，需使用Final来实现准实时。参考https://developer.aliyun.com/article/781084。
Insert + argMax，表引擎使用ReplacingMergeTree，argMax(field1，field2): 按照 field2 的最大值取field1的值。在创建表结构的时候，指定版本列ver，在合并时，会保留ver值最大的版本。参考https://cloud.tencent.com/developer/article/1644570



### CK基本概念

ClickHouse: ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) for online analytical processing (OLAP).
OLAP: OLAP scenarios require real-time responses on top of large datasets for complex analytical queries with the following characteristics:

- Datasets can be massive - billions or trillions of rows
- Data is organized in tables that contain many columns
- Only a few columns are selected to answer any particular query
- Results must be returned in milliseconds or seconds
  Column-Oriented vs Row-Oriented Databases: 
- In a row-oriented DBMS, data is stored in rows, with all the values related to a row physically stored next to each other.
- In a column-oriented DBMS, data is stored in columns, with values from the same columns stored together.

行式存储的好处: 想查找某个人所有的属性时，可以通过一次磁盘查找加顺序读取就可以；但是当想查所有人的年龄时，需要不停的查找，或者全表扫描才行，遍历的很多数据都是不需要的。
列式存储的好处: 

- 对于列的聚合、计数、求和等统计操作优于行式存储
- 由于某一列的数据类型都是相同的，针对于数据存储更容易进行数据压缩，每一列选择更优的数据压缩算法，大大提高了数据的压缩比重
- 数据压缩比更好，一方面节省了磁盘空间，另一方面对于cache也有了更大的发挥空间
- 列式存储不支持事务

### CK使用

1. 连接: clickhouse client --user 'soc' --password 'Q!hooS0c'
2. 创建数据库: clickhouse-client --query "CREATE DATABASE IF NOT EXISTS tutorial"
3. 创建数据表:

 - 要创建的表的名称。
 - 表结构，例如：列名和对应的数据类型。
 - 表引擎及其设置，这决定了对此表的查询操作是如何在物理层面执行的所有细节。

### 数据库引擎&表引擎

ClickHouse默认使用Atomic数据库引擎，支持非阻塞的DROP TABLE和RENAME TABLE查询和原子的EXCHANGE TABLES t1 AND t2查询。
表引擎: 表引擎（即表的类型）决定了：

- 数据的存储方式和位置，写到哪里以及从哪里读取数据。
- 支持哪些查询以及如何支持。
- 并发数据访问。
- 索引的使用（如果存在）。
- 是否可以执行多线程请求。
- 数据复制参数。

表引擎分类:

- MergeTree 合并树家族: 适用于高负载任务的最通用和功能最强大的表引擎。这些引擎的共同特点是可以快速插入数据并进行后续的后台数据处理。MergeTree系列引擎支持数据复制（使用Replicated* 的引擎版本），分区和一些其他引擎不支持的其他功能。参考：https://clickhouse.com/docs/zh/engines/table-engines/mergetree-family/mergetree

- MergeTree 系列的引擎被设计用于插入极大量的数据到一张表当中。数据可以以数据片段的形式一个接着一个的快速写入，数据片段在后台按照一定的规则进行合并。相比在插入时不断修改（重写）已存储的数据，这种策略会高效很多。
  主要特点:
  存储的数据按主键排序。这使得您能够创建一个小型的稀疏索引来加快数据检索。建表时如果没有使用 `PRIMARY KEY` 显式指定的主键，ClickHouse 会使用排序键作为主键。ClickHouse 不要求主键唯一，所以可以插入多条具有相同主键的行。
  如果指定了 分区键 的话，可以使用分区。
  在相同数据集和相同结果集的情况下 ClickHouse 中某些带分区的操作会比普通操作更快。查询中指定了分区键时 ClickHouse 会自动截取分区数据。这也有效增加了查询性能。
  支持数据副本。ReplicatedMergeTree 系列的表提供了数据副本功能。
  支持数据采样。

  ReplacingMergeTree: 引擎和MergeTree的不同之处在于它会删除排序键值相同的重复项。它适用于在后台清除重复的数据以节省空间，但是它不保证没有重复的数据出现。
  SummingMergeTree: 引擎继承自MergeTree，不同之处，当合并 SummingMergeTree 表的数据片段时，ClickHouse 会把所有具有相同主键的行合并为一行，该行包含了被合并的行中具有数值数据类型的列的汇总值。如果主键的组合方式使得单个键值对应于大量的行，则可以显著的减少存储空间并加快数据查询的速度。
  AggregatingMergeTree: 引擎继承自 MergeTree，并改变了数据片段的合并逻辑。 ClickHouse 会将一个数据片段内所有具有相同主键（准确的说是 排序键）的行替换成一行，这一行会存储一系列聚合函数的状态。
  CollapsingMergeTree: 该引擎继承于 MergeTree，并在数据块合并算法中添加了折叠行的逻辑。CollapsingMergeTree 会异步的删除（折叠）这些除了特定列 Sign 有 1 和 -1 的值以外，其余所有字段的值都相等的成对的行。没有成对的行会被保留。更多的细节请看本文的折叠部分。
  VersionedCollapsingMergeTree： 引擎继承自 MergeTree 并将折叠行的逻辑添加到合并数据部分的算法中。 VersionedCollapsingMergeTree允许以多个线程的任何顺序插入数据。 特别是， Version 列有助于正确折叠行，即使它们以错误的顺序插入。 相比之下, CollapsingMergeTree 只允许严格连续插入。

- 日志引擎: 具有最小功能的轻量级引擎。当您需要快速写入许多小表（最多约100万行）并在以后整体读取它们时，该类型的引擎是最有效的。该类型的引擎：TinyLog/StripeLog/Log

- 集成引擎: 用于与其他的数据存储与处理系统集成的引擎。该类型的引擎：Kafka/MySQL/ODBC/JDBC/HDFS

- 用于其他特定功能的引擎: Memory...



### 其他

建表: 

```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1] [TTL expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2] [TTL expr2],
    ...
    INDEX index_name1 expr1 TYPE type1(...) GRANULARITY value1,
    INDEX index_name2 expr2 TYPE type2(...) GRANULARITY value2
) ENGINE = MergeTree()
ORDER BY expr
[PARTITION BY expr]
[PRIMARY KEY expr]
[SAMPLE BY expr]
[TTL expr [DELETE|TO DISK 'xxx'|TO VOLUME 'xxx'], ...]
[SETTINGS name=value, ...]
```

分区：MergeTree 系列的表（包括 可复制表 ）可以使用分区。分区是在一个表中通过指定的规则划分而成的逻辑数据集。可以按任意标准进行分区，如按月，按日或按事件类型。为了减少需要操作的数据，每个分区都是分开存储的。访问数据时，ClickHouse 尽量使用这些分区的最小子集。分区是在建表时通过 PARTITION BY expr 子句指定的。分区键可以是表中列的任意表达式。
可以通过 system.parts 表查看表片段和分区信息。
新数据插入到表中时，这些数据会存储为按主键排序的新片段（块）。插入后 10-15 分钟，同一分区的各个片段会合并为一整个片段。

```
SELECT
    partition,
    name,
    active
FROM system.parts
WHERE table = 'event'
```

MATERIALIZED expr: 物化表达式，建表时用，被该表达式指定的列不能包含在INSERT的列表中，因为它总是被计算出来的。 对于INSERT而言，不需要考虑这些列。 另外，在SELECT查询中如果包含星号，此列不会被用来替换星号，这是因为考虑到数据转储，在使用SELECT *查询出的结果总能够被’INSERT’回表。


### CK SQL命令
系统表: [系统表 | ClickHouse Docs](https://clickhouse.com/docs/zh/operations/system-tables)
系统表提供的信息如下:
  - 服务器的状态、进程以及环境。
  - 服务器的内部进程。

系统表(https://clickhouse.com/docs/zh/operations/system-tables):
  - 存储于 `system` 数据库。
  - 仅提供数据读取功能。
  - 不能被删除或更改，但可以对其进行分离(detach)操作。
  
几个重要的系统表:
  - system.databases: 包含当前用户可用的数据库的相关信息。
  - system.parts: 此系统表包含 MergeTree 表分区的相关信息。
  - system.columns: 此系统表包含所有表中列的信息。
  - system.functions: 包含有关常规函数和聚合函数的信息。
  - system.metrics: 此系统表包含可以即时计算或具有当前值的指标。例如，同时处理的查询数量或当前的复制延迟。这个表始终是最新的。
  - system.settings: 包含当前用户会话设置的相关信息。
  - system.table_engines: 包含服务器支持的表引擎的描述及其功能支持信息。
  - system.tables: 包含服务器知道的每个表的元数据。

查看数据库数据表: 
```
show tables from system
```
查看数据表分区: 
```
SELECT name, `partition`,`partition_id`, `table`, `database` FROM system.parts
```
查看数据库: 
```
SELECT * FROM system.databases
```
删除某个数据表的某个分区的数据: 
```
ALTER TABLE ... DROP PARTITION
demo: ALTER TABLE sales DROP PARTITION 202308;

```
复制分区: 可以使用`ALTER TABLE ... REPLACE PARTITION`从一张表复制分区到另一张表，前提是两张表的字段结构和分区键完全相同，例如：
```
ALTER TABLE destination_table REPLACE PARTITION 'partition_name' FROM source_table;
```
分区的卸载和装载: 可以使用`ALTER TABLE ... DETACH PARTITION`卸载分区，使用`ALTER TABLE ... ATTACH PARTITION`装载分区，例如：
```
 ALTER TABLE your_table_name DETACH PARTITION 'partition_name'; 
 ALTER TABLE your_table_name ATTACH PARTITION 'partition_name';
```


### OLAP和OLTP扫盲

参考: https://zhuanlan.zhihu.com/p/400981139
OLAP: 联机分析处理，OLAP是数据仓库系统的主要应用，支持复杂的分析操作，侧重决策支持，并且提供直观易懂的查询结果。
OLTP: 联机事务处理，传统的关系型数据库的主要应用，主要是基本的、日常的事务处理。
维度模型的概念出自于数据仓库领域，是数据仓库建设中的一种数据建模方法。维度模型主要由事实表和维度表这两个基本要素构成。
常见的OLAP系统可以分为以下三类：关系型联机实时分析系统(Relational-OLAP，ROLAP)，多维联机实时分析系统(Multidimensional-OLAP，MOLAP)，混合型联机实时分析系统(Hybrid-OLAP，HOLAP)。


