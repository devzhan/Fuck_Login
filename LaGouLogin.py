# coding: utf8
import os

import requests
import re
import json
import hashlib
import sys
import subprocess
import time

CaptchaImagePath = QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
    'X-Requested-With': 'XMLHttpRequest',
    'Host':'passport.lagou.com',
    'Referer':'https://www.lagou.com/',
    'Upgrade-Insecure-Requests':'1',
}


class LaGou(object):
    def __init__(self, headers):
        self.headers = headers
        self.session = requests.session()


    def getCaptcha(self):
        captchaImgUrl = 'https://passport.lagou.com/vcode/create?from=register&refresh=%s' % time.time()
        # 写入验证码图片
        f = open(CaptchaImagePath, 'wb')
        f.write(self.session.get(captchaImgUrl, headers=HEADERS).content)
        f.close()
        # 打开验证码图片
        if sys.platform.find('darwin') >= 0:

            subprocess.call(['open', CaptchaImagePath])
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', CaptchaImagePath])
        else:
            os.startfile(CaptchaImagePath)

        # 输入返回验证码
        captcha = input("请输入当前地址(% s)的验证码: " % CaptchaImagePath)
        print('你输入的验证码是:% s' % captcha)
        return captcha
    def login(self, username, password, captchaData=None, token_code=None):
        postData = {
            'isValidate': 'true',
            'password': password,
            # 如需验证码,则添加上验证码
            'request_form_verifyCode': (captchaData if captchaData != None else ''),
            'submit': '',
            'username': username
        }

        url='https://passport.lagou.com/login/login.html?ts=1502506862347&serviceId=lagou&service=https%253A%252F%252Fwww.lagou.com%252F&action=login&signature=6433F428D254967E82EAC5EF2AAD49B2'
        resp = self.session.get(url,headers=self.headers)
        pattern_token=re.compile('window.X_Anti_Forge_Token = \'(.*?)\';',re.S)
        X_Anti_Forge_Token=re.findall(pattern_token,resp.text)
        pattern_code=re.compile('window.X_Anti_Forge_Code = \'(.*?)\';',re.S)
        X_Anti_Forge_Code=re.findall(pattern_code,resp.text)
        anti_token={}
        if X_Anti_Forge_Token is not None and len(X_Anti_Forge_Token)>0:
            anti_token ['X-Anit-Forge-Token']= X_Anti_Forge_Token[0]

        if X_Anti_Forge_Code is not None and len(X_Anti_Forge_Code)>0:
            anti_token ['X_Anti_Forge_Code']= X_Anti_Forge_Code[0]
        login_headers=HEADERS.copy()
        login_headers.update(anti_token)
        login_url = 'https://passport.lagou.com/login/login.json'
        response = self.session.post(login_url, data=postData, headers=login_headers)
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        if data['state'] == 1:
            return response.content
        elif data['state'] == 10010:
            print(data['message'])
            captchaData = self.getCaptcha()
            token_code = {'X-Anit-Forge-Code' : data['submitCode'], 'X-Anit-Forge-Token' : data['submitToken']}
            return self.login(username, password, captchaData, token_code)
        else:
            print(data['message'])
            return False
        pass

def encryptPwd(passwd):
    # 对密码进行了md5双重加密
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    # veennike 这个值是在js文件找到的一个写死的值
    passwd = 'veenike'+passwd+'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    return passwd
def main():
    username=input("please input user name:")
    password=input("please input password:")
    lagou = LaGou(headers=HEADERS)
    lagou.login(username,encryptPwd(password))
    pass


if __name__ == '__main__':
    main()
