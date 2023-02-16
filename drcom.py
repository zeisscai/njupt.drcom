
# -*- coding : utf-8 -*-

import os
import time
import sys
import requests
import subprocess

# enter the username and password of your drcom account here
username=""
upass=""
# urls for login
# In different college, it is different
# but you can find out what it is by doing:
# 1. use your cellphone to connect to the wifi of your computer or of your campus
# 2. visit a website, such as baidu, then the browser should jump to the login page
# 3. copy the address of this login page, and paste it to the LoginUrl below.
LoginUrl = "http://192.168.168.168/0.htm"
LogoutUrl = "http://192.168.168.168/F.htm"

ZeroMKKey = '123456'

# www.baidu.com ; www.so.com
# here is the ip addresses that used to ping, so we can find out if we are online.
# you can use ";" to seperate the ip addresses that you want to use to ping.
PingIpAddresses = "223.5.5.5"

SleepTime = 5

def login():
    data = {"DDDDD":username, 'upass':upass, '0MKKey':ZeroMKKey}
    r = requests.post(LoginUrl, data)
    if r.status_code == 200:
        print (u"login successfully!")
    else:
        print (u"login failed")
    return r

def logout():
    r = requests.get(LogoutUrl)
    if r.status_code != 200:
        print (u"logout failed")
    else:
        print (u"logout successfully")
    return r

def ping_ips(ips):
    for ip in ips.split(";"):
        ret = subprocess.Popen("ping -c 1 %s " % ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret.communicate()

        if ret.returncode == 0:
            print ("ping %s...successful!" % ip)
            return True
        else:
            print ("ping %s...failed!" % ip)

    return False

def keep_login():
    while True:
        if ping_ips(PingIpAddresses) == False:
            login()
        else:
            sys.exit()


if __name__ == "__main__":
    keep_login()
