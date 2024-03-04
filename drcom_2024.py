import requests
import configparser
import socket

def get_local_ip():
    try:
        # 创建一个UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个不存在的IP地址和端口
        sock.connect(("10.255.255.255", 1))
        # 获取本地IP地址
        ip = sock.getsockname()[0]
        return ip
    except socket.error:
        return "无法获取IP地址"

def config_ip():
    # 调用函数获取本机IP地址
    local_ip = get_local_ip()
    print("本机IP地址：", local_ip)

    config = configparser.ConfigParser()
    config.read('config.ini')
    if local_ip != "无法获取IP地址":
        config.set('Login', 'ip', local_ip)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        print("无法获取IP地址，请手动填写。")

def url():
    # 获取账号、密码和IP信息
    account = config.get('Login', 'account')
    password = config.get('Login', 'password')
    ip = config.get('Login', 'ip')
    # 构造替换后的网址
    url = "https://p.njupt.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account={}&user_password={}&wlan_user_ip={}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=en&v=2123&lang=en".format(account, password, ip)

def get_it():
# 发送GET请求
    response = requests.get(url)
    content = response.text
    # 判断登录状态
    if 'dr1003({"result":0,"msg":"AC999","ret_code":2});' in content:
        print("已经在线：",content)
    elif 'dr1003({"result":1,"msg":"Portal protocol authentication succeeded!"});' in content:
        print("登录成功：",content)
    else:
        print("登录失败，错误代码：",content)


if __name__ == "__main__":
    
