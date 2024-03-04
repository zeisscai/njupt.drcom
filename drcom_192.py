# -*- coding : utf-8 -*-

import os
import time
import sys
import requests
import subprocess


username=""
upass=""

LogoutUrl = "http://192.168.168.168/F.htm"

ZeroMKKey = '123456'

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
