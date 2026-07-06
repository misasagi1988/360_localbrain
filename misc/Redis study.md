# Redis study

标签（空格分隔）： 未分类

---

当前本脑环境redis版本: 6.2.11
连接redis cmd:
./redis-cli -h 127.0.0.1 -p 6379 -a cloud@qihoo.com
command help, 查看命令帮助文档

### redis基本数据结构
分别有简单动态字符串(SDS)、链表、字典、跳跃表、整数集合以及压缩列表，它们是redis数据结构的基本组成部分。
Redis自己构建了一种简单动态字符串SDS的抽象类型，并将其用作默认字符串表示。
链表(linkedlist): 提供了高效的节点重排能力，以及顺序性的节点访问方式，并且可以通过增删节点来灵活地调整链表的长度。双端无环链表，节点带有prev和next指针。
字典(hashtable): 哈希冲突，rehash
跳跃表(skiplist): ignore
整数集合(intset)
压缩列表(ziplist): 压缩列表是Redis为了节约内存而开发的，由一系列特殊编码的连续内存块组成的顺序型（sequential）数据结构。

### redis数据类型
cmd: 
type key, 查看key对应value的数据类型
object encoding key, 查看key对应value的编码方式
- string
最大长度限制：512 MB。
如果一个字符串对象保存的是整数值，并且这个整数值可以用long类型来表示，那么字符串对象会将整数值保存在字符串对象结构的ptr属性里面（将 void* 转换成long）， 并将字符串对象的编码设置为int。
如果字符串对象保存的是一个字符串值，并且这个字符串值的长度大于等于36字节，那么字符串对象将使用一个动态字符串(SDS)来保存这个字符串值，并将对象的编码设置为raw。
如果字符串对象保存的是一个字符串值，并且这个字符串值的长度小于36字节，那么字符串对象将使用embstr编码的方式来保存这个字符串值。
- list
列表对象的编码可以是ziplist或者linkedlist。
列表对象保存的所有字符串元素的长度都小于64字节并且保存的元素数量小于512个，使用ziplist编码；否则使用linkedlist。
- hash
哈希对象的编码可以是ziplist或者hashtable。
哈希对象保存的所有键值对的键和值的字符串长度都小于64字节并且保存的键值对数量小于512个，使用ziplist编码；否则使用hashtable。
- set
集合对象的编码可以是intset或者hashtable。
集合对象保存的所有元素都是整数值并且保存的元素数量不超过512个，使用intset编码；否则使用hashtable。
- sorted set
有序集合的编码可以是ziplist或者skiplist。
有序集合保存的元素数量小于128个并且保存的所有元素成员的长度都小于64字节。使用 ziplist编码；否则使用skiplist。


- big keys
在Redis中，一个字符串最大512MB，一个二级数据结构（例如hash、list、set、zset）可以存储大约40亿个(2^32-1)个元素，但实际上中如果下面两种情况，就会认为它是bigkey:
字符串类型：它的big体现在单个value值很大，一般认为超过10KB就是bigkey。
非字符串类型：哈希、列表、集合、有序集合，它们的big体现在元素个数太多。
危害:
 - 内存空间不均匀: 不利于集群对内存的统一管理，存在丢失数据的隐患。
 - 超时阻塞: 由于Redis单线程的特性，操作bigkey的通常比较耗时，也就意味着阻塞Redis可能性越大，这样会造成客户端阻塞或者引起故障切换，它们通常出现在慢查询中。
 - 网络拥塞: 每次获取要产生的网络流量较大
 - 迁移困难
由于开发人员对Redis的理解程度不同，在实际开发中出现bigkey在所难免，重要的能通过合理的检测机制及时找到它们，进行处理。作为开发人员应该在业务开发时不能将Redis简单暴力的使用，应该在数据结构的选择和设计上更加合理，例如出现了bigkey，要思考一下可不可以做一些优化(例如二级索引)尽量的让这些bigkey消失在业务中，如果bigkey不可避免，也要思考一下要不要每次把所有元素都取出来(例如有时候仅仅需要hmget，而不是hgetall)，删除也是一样，尽量使用优雅的方式来处理。
./redis-cli --bigkeys: 查看bigkeys
- memory usage
memory usage命令可以计算每个键值的字节数（自身、以及相关指针开销)
cmd: memory usage key
对于bigkey，尽可能本地化

