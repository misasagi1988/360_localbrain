# 本脑安装-单独安装SAE引擎

标签（空格分隔）： 360BrainSecurity

---

1. soc主机针对新的sae主机开放端口
 - 26379
 - 6379
 - 2900
 - 3399
 - 9092
 - 7848
 - 8848
 - 9848
 - 9849

cmd: firewall-cmd --permanent --add-rich-rule 'rule family=ipv4 source address=172.16.5.55  port port=26379 protocol=tcp accept'  --permanent
配置完成后
firewall-cmd   --reload

2. 找到原来的安装配置文件和安装包，传到新的机器上

3. 老的配置文件中，修改如下
   IP=10.39.170.131,10.39.170.132,10.39.170.134,10.39.170.135   新增sae的ip，比如10.39.170.135
   SAE_CORE_IP_PORT=10.39.170.132:8765,10.39.170.134:8765,10.39.170.135:8765   新增sae的ip和port，比如,10.39.170.135:8765



