
tomcat本地配置迁移到nacos



发布配置文件到nacos特定命名空间：curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?namespaceId=fb8185d5-8caf-4583-b3df-8f56395dea84&group=DEV_GROUP&dataId=application.properties&content=username%3Dadmin"