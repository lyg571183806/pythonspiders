# -*- coding:utf-8 -*-

__author__ = 'yunshu'

import urllib
import urllib2
import re
import thread
import time

#糗事百科爬虫类
class QSBK:
    pageIndex = 1
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    # #存放段子的变量
    stories = []
    enable = False

    def __init__(self):
        pass

    # def __init__(self):
    #     self.pageIndex = 1
    #     self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    #     self.headers = {'User-Agent' :self.user_agent}
    #     self.stories = []
    #     self.enable = False

    #获取页面内容
    def getPage(self, pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageinfo = response.read().decode('utf-8')
            return pageinfo
        except urllib2.URLError, e:
            if hasattr(e, 'reasion'):
                print u"连接糗事百科失败，错误原因",e.reason
                return None

    #获取一页的段子列表
    def getPageItems(self, pageIndex):
        pageinfo = self.getPage(pageIndex)
        if not pageinfo:
            print u"页面加载失败"
            return None
        pattern = re.compile('h2>(.*?)</h2.*?content">.*?<span>(.*?)</span>.*?number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageinfo)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])

        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1;

    #显示段子信息
    def getOneStroy(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u"第%d页，发布人：%s,赞：%s\n%s" % (page, story[0], story[2], story[1])

    def start(self):
        print u"正在去读糗事百科，按回车查看段子，Q退出"
        self.enable = True
        self.loadPage()
        newpage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                newpage +=1
                del self.stories[0]
                self.getOneStroy(pageStories, newpage)


spider = QSBK()
spider.start()