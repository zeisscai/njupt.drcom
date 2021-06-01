# njupt.drcom 上网登陆脚本
南京邮电大学校园网上网登陆脚本
南邮校园网上网登陆脚本

本项目完全参考[hisaner/Drcom-Padavan](https://github.com/hisaner/Drcom-Padavan/blob/main)

hostname=10.10.244.11
wlanacip=10.165.255.254（仙林宿舍北区、大学生活动中心）

wlanacname=XL-BRAS-SR8806-X&mac=00-00-00-00-00-00

标准的上网登陆网址：
http://10.10.244.11/a70.htm?wlanuserip=内网地址&wlanacip=10.165.255.254&wlanacname=XL-BRAS-SR8806-X

按照原文操作即可。
## 补充说明
第二个sleep 5s在mac和pandoraBox中会报错，但是不影响运行。

注意脚本在获得内网地址的设备上运行，否则CURRENT_IP无法正确获取。

路由器缺失curl的话安装一下就好了，软件包名称：curl，自动安装依赖。

# 对照下图补充修改就可以了
![4.42.13.jpg](https://i.loli.net/2021/06/01/izoITGnDBNkLAwS.jpg)

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
