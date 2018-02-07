# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os

#抓取淘女郎的信息
class Spider:
    def __init__(self):
        self.baseURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
    def getPage(self, pageNum):
        try:
            geturl = 'https://mm.taobao.com/json/request_top_list.htm?page=' + str(pageNum)
            # print geturl
            # httpHandler = urllib2.HTTPHandler(debuglevel=1)
            # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
            # opener = urllib2.build_opener(httpHandler, httpsHandler)
            # urllib2.install_opener(opener)
            request = urllib2.Request(geturl, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read().decode('gbk')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print "链接淘女郎失败，失败原因：" + e.reason
                return None

    def getDetailPage(self, pageUrl):
        location = pageUrl.split('/')
        user_id = location.pop().replace('.htm','')
        url = 'https://mm.taobao.com/self/model_info.htm?user_id='+user_id
        pageinfo  =urllib2.urlopen(url)
        return pageinfo.read().decode('gbk')

    def getBrief(self, detailPage):
        # re.compile('')
        pass

    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        # print fileName
        # return
        f = open(fileName, 'wb')
        f.write(data)
        print "正在偷偷地保存了他的一张图片"
        f.close()

    def saveIcon(self, imageURL, name):
        fileName = name + '/icon.jpg'
        self.saveImg(imageURL, fileName)

    def makeDir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print '偷偷地创建了名字叫做',path,'的文件夹'
            os.makedirs(path)
            return True
        else:
            print "已经创建了",path,"文件夹"
            return False

    def saveTextFile(self, content, name):
        fileName = name + '.txt'
        f = open(fileName, 'w+')
        print "正在偷偷地保存她的个人信息为：",fileName
        f.write(content.encode('utf-8'))

    def getContents(self, pageNum):
        page = self.getPage(pageNum)
        # print contents
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append(['http:'+item[0],'http:'+item[1],item[2],item[3],item[4]])

        return contents

    def savePageInfo(self, pageNum):
        contents = self.getContents(pageNum)
        for item in contents:
            print "发现一位模特，名字叫",item[2],"，芳龄",item[3],"，她在",item[4],"头像地址",item[1]
            print "正在偷偷地保存她的信息"
            print "又意外地发现她的个人地址是",item[0]

            #个人详情页
            detailUrl = item[0]
            detailPage = self.getDetailPage(detailUrl)
            #获取个人简介
            brief = self.getBrief(detailPage)
            # self.makeDir(item[2])
            #保存个人简介
            # self.saveTextFile(content, item[2])
            #保存个人头像
            # self.saveIcon(item[1], item[2])

    def start(self, start, end):
        for i in range(start, end+1):
            print "正在偷偷寻找第",i,"个地方，看看MM在不在"
            self.savePageInfo(i)

spider = Spider()
spider.start(1, 2)