# coding: utf8
import requests
from bs4 import BeautifulSoup
import random
import re
from PIL import Image
import os
try:
    import cookielib
except:
    import http.cookiejar as cookielib

class ZhenAi(object):
    def __init__(self,headers):
        self.headers=headers
        self.session=requests.session()



        pass
    def login(self,username,password):
        self.session.cookies = cookielib.LWPCookieJar(filename='zhanaicookies')
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")
        loginUrl='http://profile.zhenai.com/login/login.jsp?fromurl=http://profile.zhenai.com/v2/personal/home.do'
        pageContent=self.session.get(loginUrl,headers=self.headers)
        soup=BeautifulSoup(pageContent.text,"lxml")
        # print(soup)
        codePattern = re.compile('<img id="codeImg" src="(.*?)">',re.S);
        result=re.findall(codePattern,pageContent.text)
        if result :
            captcha_url='http://profile.zhenai.com'+result[0]


        r = self.session.get(captcha_url)
        with open('zhenai.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        try:
            im = Image.open('zhenai.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到zhenai.jpg 手动输入' % os.path.abspath('zhenai.jpg'))
        code=input("please input verify code:")

        data={
            'fromurl':'http://profile.zhenai.com/v2/personal/home.do',
            'loginZAT':'0',
            'formHuntWedding':'',
            'whichTV':'',
            'fid':'',
            'mid':'',
            'redirectUrl':'',
            'isTpRedirect':'',
            'loginmode':'2',
            'whereLogin':'login_page',
            'rememberpassword':'1',
            'loginInfo':username,
            'password':password,
            'imgCode':code
        }
        postUrl='http://profile.zhenai.com/login/loginactionindex.jsps'
        loginContent=self.session.post(postUrl,data=data,headers=self.headers)
        print(loginContent.text)
        self.session.cookies.save()
        userUrl='http://profile.zhenai.com/v2/userdata/showRegInfo.do'
        userContent=self.session.get(userUrl,headers=self.headers)
        print(userContent.text)

        pass



def main():
    username = input('请输入你的用户名：')
    password = input('请输入密码：')
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'profile.zhenai.com'
}
    zhenAi=ZhenAi(headers=headers)
    zhenAi.login(username,password)

    pass


if __name__ == '__main__':
     main()
