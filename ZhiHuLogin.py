# coding: utf8
import requests
from bs4 import BeautifulSoup
import time
import os


class ZhiHuLogin(object):
    def __init__(self, headers):
        self.headers = headers;
        self.session = requests.session()
        pass

    def login(self, username, password):
        webUrl = "https://www.zhihu.com"
        data = {'is_org_page': 'false'}
        resp = self.session.get(webUrl, data=data, headers=self.headers)
        homesoup = BeautifulSoup(resp.text, "html.parser")
        xsrfinput = homesoup.find('input', {'name': '_xsrf'})
        xsrf_token = xsrfinput['value']
        print("获取到的xsrf_token为： ", xsrf_token)
        self.getCap()
        # userName=input("please input your name:")

        self.headers['X-Xsrftoken'] = xsrf_token
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        loginurl = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': xsrf_token,
            'email': username,
            'password': password
        }
        loginresponse = self.session.post(url=loginurl, headers=self.headers, data=postdata)
        print(loginresponse.json())
        if loginresponse.json()['r'] == 1:
            self.getCap()
            captcha = input('请输入验证码：')
            postdata['captcha'] = captcha
            loginresponse = self.session.post(url=loginurl, headers=self.headers, data=postdata)
            print('服务器端返回响应码：', loginresponse.status_code)
            print(loginresponse.json())
        profileurl = 'https://www.zhihu.com/settings/profile'
        profileresponse = self.session.get(url=profileurl, headers=self.headers)
        print('profile页面响应码：', profileresponse.status_code)
        profilesoup = BeautifulSoup(profileresponse.text, 'html.parser')
        div = profilesoup.find('div', {'id': 'rename-section'})
        print(div)

    def getCap(self):
        randomtime = str(int(time.time() * 1000))
        captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                     randomtime + "&type=login"
        captcharesponse = self.session.get(url=captchaurl, headers=self.headers)
        with open('checkcode.gif', 'wb') as f:
            f.write(captcharesponse.content)
            f.close()


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'X-Requested-With': 'XMLHttpRequest'
    }
    zhihu = ZhiHuLogin(headers=headers)
    userName = input("please input your name:")
    passWord = input("please input your password:")
    zhihu.login(userName, passWord)
    pass


if __name__ == '__main__':
    main()
