import requests
from lxml import etree
import urllib
import os
import sys
import time
import re
import random
# proxies = [
#     {
#         'http': 'http://137.27.142.226:54922',
#         'https': 'https://137.27.142.226:54922',
#     },
#     {
#         'http': 'http://62.4.54.158:53102',
#         'https': 'https://62.4.54.158:53102',
#     },
#     {
#         'http': 'http://189.124.195.185:37318',
#         'https': 'https://189.124.195.185:37318',
#     },
#     {
#         'http': 'http://197.219.200.20:47369',
#         'https': 'https://197.219.200.20:47369',
#     },
# ]
head = [
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    },
    {
        'user-agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    },
    {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    },
    {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    },
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
    },
    {
        'user-agent': 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0'
    },
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    },
    {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
    }
]
def getwebpage(url):
    time.sleep(1)

    resp=requests.get(url,cookies={'over18':'1'},headers=random.choice(head))
    if resp.status_code!=200:
        print('Invaild url',resp.url)
        return None
    else:
        return resp.text
#文章標題
def getarticles(dom):
    print(dom)
    html =etree.HTML(dom)
    title=html.xpath('//div[@class="title"]/a/text()')
    return title
#文章連結
def getTitlehref(dom):
    html=etree.HTML(dom)
    href = html.xpath('//div[@class="title"]/a/@href')
    return href
#上一頁連結
def getlast(dom):
    html=etree.HTML(dom)
    last = html.xpath('//a[@class="btn wide"]/@href')[1]
    return last
#獲取圖片連結
def getImageHref(href,title):
    count=0
    for article_url in href:
        page = getwebpage(PTT_URL+article_url)                                       #------------獲取文章網頁
        html = etree.HTML(page)                                                      #------------XML
        link = html.xpath('//*[@id="main-content"]/a[contains(@href,"imgur")]/@href')#------------尋找文章圖片連結並過濾
        if link:                                                                     #------------檢查文章裡是有有圖片連結
            SaveImage(link,title[count])
        count+=1
#存取圖片
def SaveImage(href,title):
    k = 1
    TempFileName=str(title)
    FileName = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）:]+", "", TempFileName)
    print(FileName,end='\n')
    folder=os.path.exists(FileName)
    if folder:
        print(FileName+"目錄已存在")
    else:
        os.makedirs(FileName)
        for i in range(len(href)):
            number = str(k)
            urllib.request.urlretrieve(
            href[i], os.path.join(FileName, number+".jpg"))
            print(k)
            k = k+1

if __name__ == "__main__":
    PTT_URL = "https://www.ptt.cc/"
    page = getwebpage('https://www.ptt.cc/bbs/Beauty/index.html')
    Title=[]
    count=input("輸入你要抓的頁數:")
    count=int(count)
    for i in range(count):
        if i!=0:
            last = getlast(page)
            page = getwebpage(PTT_URL+last)
        title = getarticles(page)
        for each in title:
            Title.append(each)
        href = getTitlehref(page)
        getImageHref(href,Title)
        Title=[]
    pass
