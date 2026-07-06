# Rocksdb study

标签（空格分隔）： 未分类

---
### 文件介绍
*.log: 事务日志用于保存数据操作日志，可用于数据恢复
*.sst: 数据持久换文件
MANIFEST：数据库中的MANIFEST文件记录数据库状态。压缩过程会添加新文件并从数据库中删除旧文件，并通过将它们记录在 MANIFEST 文件中使这些操作持久化。
CURRENT：记录当前正在使用的MANIFEST文件
LOCK：rocksdb自带的文件锁，防止两个进程来打开数据库。

### LSM简介
https://blog.csdn.net/qq_32907195/article/details/116754715
https://cloud.tencent.com/developer/article/1143750

LSM树: Log-Structured-Merge-Tree，LSM树会将所有的数据插入、修改、删除等操作记录(注意是操作记录)保存在内存之中，当此类操作达到一定的数据量后，再批量地顺序写入到磁盘当中。这与B+树不同，B+树数据的更新会直接在原数据所在处修改对应的值，但是LSM数的数据更新是日志式的，当一条数据更新是直接append一条更新记录完成的。这样设计的目的就是为了顺序写，不断地将Immutable MemTable flush到持久化存储即可，而不用去修改之前的SSTable中的key，保证了顺序写。
因此当MemTable达到一定大小flush到持久化存储变成SSTable后，在不同的SSTable中，可能存在相同Key的记录，当然最新的那条记录才是准确的。这样设计的虽然大大提高了写性能，但同时也会带来一些问题：
1）冗余存储，对于某个key，实际上除了最新的那条记录外，其他的记录都是冗余无用的，但是仍然占用了存储空间。因此需要进行Compact操作(合并多个SSTable)来清除冗余的记录。
2）读取时需要从最新的倒着查询，直到找到某个key的记录。最坏情况需要查询完所有的SSTable，这里可以通过前面提到的索引/布隆过滤器来优化查找速度。

LSM树的Compact策略：size-tiered和leveled。
size-tiered策略保证每层SSTable的大小相近，同时限制每一层SSTable的数量。每层限制SSTable为N，当每层SSTable达到N后，则触发Compact操作合并这些SSTable，并将合并后的结果写入到下一层成为一个更大的sstable。
由此可以看出，当层数达到一定数量时，最底层的单个SSTable的大小会变得非常大。并且size-tiered策略会导致空间放大比较严重。即使对于同一层的SSTable，每个key的记录是可能存在多份的，只有当该层的SSTable执行compact操作才会消除这些key的冗余记录。
leveled策略也是采用分层的思想，每一层限制总文件的大小。但是跟size-tiered策略不同的是，leveled会将每一层切分成多个大小相近的SSTable。这些SSTable是这一层是全局有序的，意味着一个key在每一层至多只有1条记录，不存在冗余记录。
leveled策略相较于size-tiered策略来说，每层内key是不会重复的，即使是最坏的情况，除开最底层外，其余层都是重复key，按照相邻层大小比例为10来算，冗余占比也很小。因此空间放大问题得到缓解。但是写放大问题会更加突出。举一个最坏场景，如果LevelN层某个SSTable的key的范围跨度非常大，覆盖了LevelN+1层所有key的范围，那么进行Compact时将涉及LevelN+1层的全部数据。

RocksDB的每个键值对都与唯一一个列族（column family）结合。如果没有指定Column Family，键值对将会结合到“default” 列族。不同的Column Family共享WAL，独享sst和memtable，所以Column Family起到了一定的逻辑和资源隔离的作用。

### RocksDB调优
调优RocksDB通常就是在三个放大因子间做权衡：写放大，读放大，和空间放大。
写放大: 写入磁盘的数据与写入数据库的字节数的比。一个数据会随着Compaction过程向更高的层重复写入，有多少层就写多少次。如果写放大很高，工作负载的瓶颈可能在磁盘吞吐。
读放大: 读取一次数据会产生多次的io，即为读放大，SSL读取顺序为内存->存储0level->存储nlevel，最坏的可能要读取到n level（每一层io一次）。
空间放大: 指存储引擎的数据实际占用的磁盘空间比数据的真正大小偏多的情况。

https://www.cnblogs.com/lygin/p/17158774.html
### 调优参数
#### Block Cache 系列参数
Block Size
Block Cache Size
如果需要增加 Block Size 的大小来提升读写性能，请务必一并增加 Block Cache Size（接下来要介绍）的大小，这样才可以取得比较好的读写性能。如果内存已经吃紧，那么不建议继续增加 Block Cache Size，否则会有 OOM 的风险。
#### Index 和 Bloom Filter 系列参数
每个 SST 都可以有一个索引（Index）和 Bloom Filter（布隆过滤器），他们可以提升读性能，因为有了索引，不必顺序遍历整个 SST 文件，就可以定位具体的 Key 在哪里，因为已经保存了所有的 Key、Offset、Size 等元数据；而通过布隆过滤器，可以在假阳（False Positive）率很低的情况下，迅速判断某个 Key 是否在这个 SST 文件中，如果返回 False 就不再继续找索引了。
cache_index_and_filter_blocks：默认false，表示不在内存里缓存索引和过滤器 Block，而是用到了载入，不用就踢出去。如果设置为 true，则表示允许把这些索引和过滤器放到 Block Cache 中备用，这样可以提升局部数据存取的效率。但是，如果启用了这个选项，必须同时把 pin_l0_filter_and_index_blocks_in_cache（blockBasedTableConfig.pinL0FilterAndIndexBlocksInCache）参数也设置为 true。
optimize_filters_for_hits: 这个参数（columnFamilyOptions.setOptimizeFiltersForHits）如果设置为 true，则 RocksDB 不会给 L0 生成 Bloom Filter，据文档中描述，可以减少 90% 的 Filter 存储开销，有利于减少内存占用。但是，这个参数也仅仅适合于具有局部热点或者确信基本不会出现 Cache Miss 的场景，否则频繁的找不到，会拖累读取性能。
#### MemTable 系列参数
Write Buffer Size，这个参数的调整，必须随着下面的几个参数一起来做，否则可能会达不到预期的效果。
Max Bytes For Level Base，如果增加 Write Buffer Size，请一定要适当增加 L1 层的大小阈值（max_bytes_for_level_base），这个因子影响非常非常大。
Write Buffer Count，可以控制内存中允许保留的 MemTable 最大个数
Min Write Buffer Number To Merge，决定了 Write Buffer 合并的最小阈值，默认值为 1，对于机械硬盘来说可以适当调大，避免频繁的 Merge 操作造成的写停顿。
#### Flush 和 Compaction 相关参数
RocksDB 的后台进程中，有持续不断的 Flush 和 Compaction 操作。前者将 MemTable 的内容刷写到磁盘的 SST 文件中；后者则会对多个 SST 文件做归并和重整，删除重复值，并向更高的层级（Level）移动。例如 L0 -> L1 等。
频繁的 Flush 和 Compaction 操作，在写数据量大时，会严重影响性能，甚至造成写入的完全停顿，即 Write Stall，因此这里也需要进行细致的调优。

// block cache
block_cache_usage: 
// blocks pinned by iterator
block_cache_pinned_usage
// indexes and filter blocks
indexes_and_filter_block_usage: 
// mem-table, get the current memtable size
mem_table_usage: 
cur_size_all_mem_tables: 