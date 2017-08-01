# coding: utf8
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
# 登录csdn 评论文章，点赞文章，发送私信
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
        if response.status_code==200:
            result=re.findall(userPattern,content)
            if result:
                print("登录成功")
                print(result)
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
if __name__=="__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
    # Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0
    }
    csdn = CSDN(headers=headers)
    account = input('请输入您的账号：')
    password = input('请输入您的密码:')
    csdn.login(account,password)
    commentUrl='http://blog.csdn.net/waniu123/article/details/54580680'
    csdn.comment(commentUrl,"爬虫测试")
    csdn.digg(commentUrl,False)
    csdn.letter("jackroyal",content='爬虫私信，收到请回复，Over！')
