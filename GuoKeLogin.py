# coding: utf8
import requests
from bs4 import BeautifulSoup
import os
import sys

url='https://account.guokr.com/sign_in/?success=https%3A%2F%2Faccount.guokr.com%2Foauth2%2Fauthorize%2F%3Fclient_id%3D32353%26redirect_uri%3Dhttps%253A%252F%252Faccount.guokr.com%252Fsso%252F%253Flazy%253Dy%2526rid%253D1772169362%2526success%253Dhttps%25253A%25252F%25252Faccount.guokr.com%25252F%26response_type%3Dcode%26state%3Dc706030ede4fed074f7ebd6f0459555e5ad1fe22e9647b64c6a624972662f331--1502289336%26suppress_prompt%3D1'

class GuoKe(object):
    def __init__(self,headers):
        self.headers=headers
        self.session=requests.Session()
        self.url='https://account.guokr.com/sign_in/?success=https%3A%2F%2Faccount.guokr.com%2Foauth2%2Fauthorize%2F%3Fclient_id%3D32353%26redirect_uri%3Dhttps%253A%252F%252Faccount.guokr.com%252Fsso%252F%253Flazy%253Dy%2526rid%253D1772169362%2526success%253Dhttps%25253A%25252F%25252Faccount.guokr.com%25252F%26response_type%3Dcode%26state%3Dc706030ede4fed074f7ebd6f0459555e5ad1fe22e9647b64c6a624972662f331--1502289336%26suppress_prompt%3D1'
        resp =self.session.get(self.url)  # We'll make post requests to ``resp.url``.
        self.soup = BeautifulSoup(resp.text, "html.parser")

    def login(self,url, username, password, csrf_token, captcha, captcha_rand):
        payload = {
            "username": username,
            "password": password,
            "csrf_token": csrf_token,
            "captcha": captcha,
            "captcha_rand": captcha_rand,
            "permanent": "y"
        }
        try:
            resp = self.session.post(url, data=payload)
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            soup = BeautifulSoup(resp.text, "html.parser")
            error = soup.find(class_="login-error")
            sys.exit(error.string.strip())

        pass
    def get_csrf_token(self):
        csrf_token = self.soup.find(id="csrf_token").attrs["value"]
        print(csrf_token)
        return csrf_token
        pass
    def get_captcha_rand(self):
        captcha_rand = self.soup.find(id="captchaRand").attrs["value"]
        print(captcha_rand)
        return captcha_rand
    def get_captcha_img(self):
        captcha_img_url = self.soup.find(id="captchaImage").attrs["src"]
        resp = self.session.get(captcha_img_url, stream=True)
        with open("captcha_img.png", "wb") as f:
            for chunk in resp.iter_content(chunk_size=128):
                f.write(chunk)

    def is_logged_in(self):
        url = "http://www.guokr.com/settings/profile/"
        resp = self.session.get(url)
        print(resp.text)
        if "gheaderSettings" in resp.text:
            return True
        else:
            return False


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    # Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0
    }
    print(12)
    guoKe = GuoKe(headers=headers)
    csrf_token=guoKe.get_csrf_token()
    captcha_rand=guoKe.get_captcha_rand()
    guoKe.get_captcha_img()
    captcha = input("Enter CAPTCHA ({})> "
                    .format(os.path.abspath("captcha_img")))
    username = input("Enter username> ")
    password = input("Enter password> ")

# login(self,url, username, password, csrf_token, captcha, captcha_rand):
    guoKe.login(url,username,password,csrf_token,captcha,captcha_rand)

    if guoKe.is_logged_in():
        print("You are now logged in.")
    else:
        print("Hmm... Something is wrong.")
    print("Cookies are save in {}".format(os.path.abspath("cookies")))

    pass


if __name__=='__main__':
    main()

