# SAE历史任务对接HQLite2.0

标签（空格分隔）： SAE_DESIGN

---


1. hql2.0流查询功能是通过StreamWsClient实现的，sae目前的做法是StreamWsClient通过服务发现创建，但目前创建StreamWsClient时就需要把StreamListener(具体消息处理类)绑定，这样不合理。预期：动态修改StreamListener

2. hql1.0转hql2.0语法需要发请求做转换实现
威胁情报相关告警输出威胁情报多个字段信息

<dependency>
  <groupId>com.hansight.hqlite</groupId>
  <artifactId>hql-client</artifactId>
  <version>2.0.0</version>
</dependency>

"index=='event' | where filter | sort occur_time | fields -original_log"

filter转换：hql-1.0 转 hql-2.0
filter: hql
source: event

http://127.0.0.1:8088/hqlite/1.0/translate
{
    "filter": "事件名称 exist",
    "source": "event"
}





