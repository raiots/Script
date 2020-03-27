# -*- coding: UTF-8 -*-
# Author:  MoeClub.org
# Adaptation: Raiot.me

import re
import sys
from urllib import request, parse
from http import cookiejar
import requests

# 请务必将 SCKEY 替换为自己的！（第63行）

account_dict = {
    '0': {'username': '用户A', 'password': '密码'},
}


def Login(URL, UserData):
    _cookies = ''
    _cookie = cookiejar.CookieJar()
    _handler = request.HTTPCookieProcessor(_cookie)
    _req = request.Request(URL, data=parse.urlencode(UserData).encode('utf-8'))
    request.build_opener(_handler).open(_req)
    for cookie in _cookie:
        _cookies += cookie.name + '=' + cookie.value + ';'
    return _cookies


def GetPage(URL, Header_Cookies):
    _Header = {'Cookie': str(Header_Cookies)}
    _req = request.Request(URL, headers=_Header)
    return request.urlopen(_req).read().decode('utf-8')


def GetCredit(user_data, proto='https'):
    username = user_data['username']
    Login_URL = proto + '://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    My_Credit = proto + '://www.hostloc.com/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1'
    My_Home = proto + '://www.hostloc.com/home.php?mod=spacecp&inajax=1'
    My_Cookies = Login(Login_URL, user_data)

    if '<td>' + str(username) + '</td>' not in GetPage(My_Home, My_Cookies):
        print('[%s] Login Fail!' % username)
    else:
        try:
            CreditNum0 = str(re.findall('[0-9]+', GetPage(My_Credit, My_Cookies))[-1])
        except:
            CreditNum0 = 'Null'
        for x in range(25297, 25309):
            GetPage(proto + '://www.hostloc.com/space-uid-{}.html'.format(x), My_Cookies)
        try:
            if CreditNum0 == 'Null':
                raise Exception
            CreditNum1 = str(re.findall('[0-9]+', GetPage(My_Credit, My_Cookies))[-1])
            if CreditNum0 == CreditNum1:
                CreditDetails = str(CreditNum1)
            else:
                CreditDetails = str(CreditNum0) + '->' + str(CreditNum1)
        except:
            CreditDetails = 'Null'
        print('[%s] Login Success! (Credit: %s)' % (username, CreditDetails))
        # 请务必将 SCKEY 替换为自己的
        sc = 'http://sc.ftqq.com/SCKEY.send?text=签到成功! ' + '[' + username + ']' + 'Credit:' + CreditDetails  
        req = requests.get(sc)
 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        n = 0
        account_dict = {}
        account_list = [sys.argv[x] for x in range(1, len(sys.argv))]
        for account in account_list:
            if ":" not in account:
                continue
            account_dict[str(n)] = {}
            account_dict[str(n)]['username'] = str(str(account).split(":", 1)[0])
            account_dict[str(n)]['password'] = str(str(account).split(":", 1)[-1])
            n += 1
    for i in range(0, len(account_dict)):
        try:
            GetCredit(account_dict[str(i)])
        except:
            continue
