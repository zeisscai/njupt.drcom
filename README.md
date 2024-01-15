# njupt.drcom 上网登陆脚本（2024）
2024-01-16更新
南邮又又更新了登陆页面，这次主要改变是登陆页面网址p.njupt.edu.cn具体的get请求url不会再浏览器网址中体现。同时登陆成功后会跳转至南邮官网。总的来说只要重新复制一下login?callback的get_url进行替换就可以了。

---
2023-07-24更新
南邮近期更新了登陆的方式，目前初步来看登陆编程了get的方式，但是从get的链接来看，暂时不清楚如何实现运营商的选择，目前暂时更新一个drcom2023.py参考。后续有空进一步开发。


---
2023-02-16更新
更新了一个适用于南邮老式上网方式的（登陆网址192.168.168.168）python3脚本。特点是使用的库都是默认库，对于自带python3的新电脑来说能直接上传使用。GitHub上好多脚本还需要先下载其他库才能使用...显然是不太方便的。


---
南京邮电大学校园网上网登陆脚本
南邮校园网上网登陆脚本

[我的博客上的教程](https://zwiss.fun/2021/07/27/%e5%8d%97%e9%82%ae%e6%a0%a1%e5%9b%ad%e7%bd%91%e8%87%aa%e5%8a%a8%e7%99%bb%e9%99%86%e8%84%9a%e6%9c%ac/)

可以挂在路由器上使用（需要刷第三方固件）推荐华硕acrh17，二手价格150左右（2021.05）刷机过程非常简单。参考我在恩山的[帖子](https://www.right.com.cn/forum/thread-4137387-1-1.html)
或者改写成windows端的脚本，然后搞个计划任务啥的。
本项目完全参考[hisaner/Drcom-Padavan](https://github.com/hisaner/Drcom-Padavan)

hostname=10.10.244.11
wlanacip=10.165.255.254（仙林宿舍北区、大学生活动中心）

wlanacname=XL-BRAS-SR8806-X&mac=00-00-00-00-00-00

标准的上网登陆网址：
http://10.10.244.11/a70.htm?wlanuserip=内网地址&wlanacip=10.165.255.254&wlanacname=XL-BRAS-SR8806-X

按照原文操作即可。

路由器里分别添加一个启动项和计划任务。

启动项：方便舍友断电重启，重连。

计划任务：每天早上7点10分登陆。

## 补充说明
第二个sleep 5s在mac和pandoraBox中会报错，但是不影响运行。

注意脚本在获得内网地址的设备上运行，否则CURRENT_IP无法正确获取。

路由器缺失curl的话安装一下就好了，软件包名称：curl，自动安装依赖。

建议将获取本机ip的命令改为：
ifconfig wlan0|grep inet|grep -v inet6|awk '{print $2}'|cut -d ':' -f2)
**openwrt可以使用上面这个**

*CURRENT_IP=$(ifconfig -a|grep inet|grep -v 127|grep -v 192|grep -v inet6|awk '{print $2}'|tr -d "addr:")
获取inet、去掉127，192字段和inet6。*

# 对照下图补充修改就可以了
![4.42.13.jpg](https://i.loli.net/2021/06/01/izoITGnDBNkLAwS.jpg)

ps，第19行还有一个要替换的CURRENT_IP。

# 原理
学校有线网络 Web 认证的本质，就是发送一个 HTTP-POST 请求到认证服务器。因此，我们只需要用 curl 构造一个 POST 请求，并且在每次路由器重启后都发送一遍即可实现自动认证。<br />
尽管不同学校的 POST 请求可能会有些许差别，但只要使用了Web认证，其原理和实现方法都是相同的。

# 抓取 HTTP POST 请求

- 使用 Chrome 的开发者工具来抓取请求：Chrome浏览器打开任意一个网站，跳转到认证页面之后，右键->检查，打开开发者工具， 选择 network，勾选 Preserve log．
- 在登录页面填写帐号密码信息，点击登录， 即可看到相关的 HTTP 请求，找到 Request Method 为 POST 的那个，右键->Copy-> Copy as cURL，即可得到认证所需的 curl 命令．使用该命令即可进行登录认证，无需在打开网页之后跳转到认证页面进行网页认证了．而 curl 支持多个平台的。
- 将复制到的 cURL 粘贴到任意文本编辑器中，以待进一步的处理。
#修改 cURL 使其永久可用
- 首先将末尾的 `--compressed --insecure`去除。分析 cURL，前大半部分都是 HTTP 请求的标头（`-H` 后的内容），`User-Agent`你可以酌情作些修改或者忽略不变不影响。
- 后面的 `--data-raw` 部分，是我们需要关注的部分。根据抓到的请求，`DDDDD=%2C0%2C` 后是我们的宽带账号，`&upass=`后是我们的宽带密码。
- 为了构造可永久使用的 cURL，首先要确保宽带账号、宽带密码是正确的。由于内网IP是由DHCP自动分配的，最后需要处理的，就是内网 IP 。在 Padavan 的 Linux 环境下，你可以使用以下命令获取当前的内网 IP：
```Bash
ifconfig | grep inet | grep -v inet6 | grep -v 127 | grep -v 192 | awk '{print $(NF-2)}' | cut -d ':' -f2
```
- 我们用变量 `CURRENT_IP`存储获得的内网IP，并在curl命令中进行了替换。需要注意的是，要在bash命令的引号中使用变量的话，引号必须为双引号，而不能采用由 Chrome 复制得来的单引号。
