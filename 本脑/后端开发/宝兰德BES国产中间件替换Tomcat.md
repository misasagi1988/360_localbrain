标签（空格分隔）： 国产中间件适配

---
bes版本：TongWeb8.0.9.04
部署环境: 11.123.244.208
部署目录: /opt/middleware/tongweb
tongweb管理控制台网页访问: 
http://11.123.244.208:9060/console
tongweb默认用户名/密码：thanos/thanos123.com
208环境密码: Q!hooS0c
wiki:  https://geelib.qihoo.net/geelib/knowledge/doc?spaceId=1384&docId=296680

10.43.102.183
环境的本脑安装目录是/opt/soc/soc，日志在/data/log/soc/bes/logs
bes端口: 1900
USER="admin"  
PASSWORD="B#2008_2108#es"

### bes操作
启动BES服务: bin/iastool --user admin --password B#2008_2108#es start --server
部署应用
bin/iastool  deploy --name "ROOT" --contextroot "/"  --type web --enabled false  ${BES_HOME}/webapps/ROOT
bin/iastool  deploy --name "sae" --contextroot "sae"  --type web --enabled false ${BES_HOME}/webapps/sae
bin/iastool  deploy --name "ice" --contextroot "ice"  --type web --enabled false ${BES_HOME}/webapps/ice
查询应用列表
bin/iastool list --application
停止应用
bin/iastool  disable --application "ROOT"
启动应用
bin/iastool  enable --application "ROOT"
停止BES服务: bin/iastool --user admin --password B#2008_2108#es stop --server