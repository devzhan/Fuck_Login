# coding: utf8
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import random
import time
import selenium
# 登录csdn 评论文章，点赞文章，发送私信
from selenium.webdriver.chrome import webdriver


class CSDN(object):
    def __init__(self,headers):
        self.headers=headers
        self.session=requests.Session()
    def login(self,account,password):
        self.account=account
        self.password=password;
        lt,execution,_eventId=self.getWebFlow()
        postData={
            'username':account,
            'password':password,
            'lt':lt,
            'execution':execution,
            '_eventId':_eventId
        }
        loginurl = 'https://passport.csdn.net/account/login'
        response=self.session.post(loginurl,headers=self.headers,data=postData)
        userPattern = re.compile('data = (.*?);',re.S);
        content=response.text
        print(response.cookies)
        if response.status_code==200:
            result=re.findall(userPattern,content)
            if result:
                print("登录成功")
                print(response.cookies)
            else:
                print("登录失败===code=="+str(response.status_code))
        else:
            print("登录失败")


    # 获取流水号
    def getWebFlow(self):
        url='https://passport.csdn.net/account/login?ref=toolbar'
        response=self.session.get(url=url,headers=self.headers)
        soup=BeautifulSoup(response.text,"html.parser")
        lt=soup.find('input',{'name':"lt"}).get("value")
        execution=soup.find('input',{'name':"execution"}).get("value")
        _eventId=soup.find('input',{'name':"_eventId"}).get("value")
        soup.clear()
        return(lt,execution,_eventId)
        pass
    # 评论
    def comment(self,articleurl,content):
        try:
            bloguser, blogid = articleurl.split('/')[3], articleurl.split('/')[-1]
            commenturl = 'http://blog.csdn.net/{}/comment/submit?id={}'.format(bloguser, blogid)
        except:
            print(commenturl, ' 不是一个合法的路径！')
        print(commentUrl)
        postdata = {
            'commentid': self.account,
            'replyid': bloguser,
            'content': content
        }
        response = self.session.post(url=commenturl, headers=self.headers, data=postdata)
        if response.status_code == 200:
            print(response.json())
            if response.json()['result'] == 1:
                print('评论成功咯！')
            else:
                print('服务器访问成功，但评论操作失败了！')
        else:
            print('评论出现了点异常！')
        pass
    #  顶 踩
    def digg(self,articleurl,digg=True):
        try:
            bloguser, blogid = articleurl.split('/')[3], articleurl.split('/')[-1]
            if digg==True:
                diggurl = 'http://blog.csdn.net/{}/article/digg?ArticleId={}'.format(bloguser, blogid)
            else:
                diggurl = 'http://blog.csdn.net/{}/article/bury?ArticleId={}'.format(bloguser, blogid)
        except:
            print(diggurl, ' 不是一个合法的路径！')
        print("待操作文章的路径： ", diggurl)
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Host'] = 'blog.csdn.net'
        self.headers['Referer'] = articleurl
        response = self.session.get(url=diggurl, headers=self.headers)
        if response.status_code == 200:
            # print("Digg 操作成功", response.text)
            articlejson = response.json()
            digg, bury = articlejson['digg'], articlejson['bury']
            print('文章：{}\n：被点赞数：{}, 被踩数：{}'.format(articleurl, digg, bury))

        else:
            print('网络或服务器出现了问题，点赞操作出现了点故障！')
        self.headers['Referer'] = ''


        # 私信
    def letter(self, receiver, content):
            letterurl = 'http://msg.csdn.net/letters/send_message?receiver={0}&body={1}'.format(receiver, quote(content))
            response = self.session.get(url=letterurl, headers=self.headers)
            if response.status_code == 200:
                print("私信内容发送成功！")
                # print(response.text)
                ## 这里服务器返回的是一大串HTML代码。通过解析还可以得到本人和其他博友的私信记录。
            else:
                print('私信发送失败！请检查网络是否通畅。')
    def publish_article(self):
        r=random.random()
        url='http://write.blog.csdn.net/postedit?edit=1&isPub=1&joinblogcontest=undefined&r='+str(r)
        userinfo1=getUserInfo1("waniu123")
        print(userinfo1)
        data={
                'titl':'hhh',                           # 博客标题
                'typ':1 ,                                 # 原创1， 转载2， 翻译3
                'cont':'333',    #  发表的文章内容
                'desc':'5555',    # 发表的摘要信息
                'tags':'python',                                  # 标签们
                'flnm':'',                        # 博客ID（如果是新文章默认没有的）
                'chnl':17,                                 # 文章类型： 编程语言啊， 系统架构啊什么的
                'comm':2,
                'level':0,
                'tag2':'android',
                'artid':0,
                'checkcode':'undefined',
                'userinfo1':userinfo1,
                'stat':'publish',
                'isauto':1
        }
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Origin'] = 'http://write.blog.csdn.net'
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.headers['Referer']='http://write.blog.csdn.net/postedit?ref=toolbar&ticket=ST-37255-sWDOprqmNHHR0dC2oSKJ-passport.csdn.net'
        self.headers['Proxy-Connection']='keep-alive'
        self.headers['Accept']= '*/*'
        self.headers['Cookie']='UserName=waniu123; UserInfo=2SLeke0bj4WbYGNZ4nqkDru0wSb5YEmb9mAonQm9%2B4%2FHiDcetzIXQNDswNwmi3a2esHk22OMmSF6MLASZOPGdDTyLcsB2Sr0rTiOil%2FH%2Fl57I6ggRciwgKiTDBC0HNJ4; UserNick=%E9%AA%91%E7%9D%80%E8%9C%97%E7%89%9B%E5%8E%BB%E8%BF%AA%E6%8B%9C; AU=FD4; UN=waniu123; UE="1427428160@qq.com"; BT=1502009214152; access-token=75be5d79-d90d-4d55-9f04-191be81a94a4; ' \
                               '_message_m=vc25qrklihznag14ueimt5br; TY_SESSION_ID=5ca5f8a0-d6a9-4e08-9185-fc59ac12dc25; __message_district_code=440000; __message_sys_msg_id=0; __message_gu_msg_id=0; __message_cnel_msg_id=0; __message_in_school=0; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1502008930,1502014993; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1502015731; dc_tos=ou9er6; dc_session_id=1502008933299_0.5533489854466307'
        response=self.session.post(url,headers=self.headers,data=data)
        print(response.url)
        print(response.text)
        pass
def getUserInfo1(un):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    d = t.split(' ');
    dd = d[0].split('-');
    ddd = d[1].split(':');
    result = int(dd[0]) + int(dd[1]) + int(dd[2]) + int(ddd[0]) + int(ddd[1]) + int(ddd[2]);
    result = result % 60;
    ascresult = 0;
    for i in un:
        ascresult += int(ord(i))
    ascresult = ascresult % 60
    unserInfo1=ascresult * result
    return unserInfo1
if __name__=="__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    # Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0
    }
    csdn = CSDN(headers=headers)
    account = input('请输入您的账号：')
    password = input('请输入您的密码:')
    csdn.login(account,password)
    print(csdn.session.cookies)
    commentUrl='http://blog.csdn.net/waniu123/article/details/54580680'
    csdn.comment(commentUrl,"爬虫测试")
    csdn.digg(commentUrl,False)
    csdn.letter("jackroyal",content='爬虫私信，收到请回复，Over！')
    csdn.publish_article()

