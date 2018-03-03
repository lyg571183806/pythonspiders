# -*- coding:utf-8 -*-
__author__ = 'yunshu'

import urllib2
import re


# 糗事百科爬虫类
class QSBK:
    page_index = 1
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/60.0.3112.113 Safari/537.36'}
    # #存放段子的变量
    stories = []
    enable = False

    def __init__(self):
        pass

    # def __init__(self):
    #     self.page_index = 1
    #     self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    #     self.headers = {'User-Agent' :self.user_agent}
    #     self.stories = []
    #     self.enable = False

    # 获取页面内容
    def get_page(self, page_index):
        try:
            url = 'https://www.qiushibaike.com/hot/page/'+str(page_index)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page_info = response.read().decode('utf-8')
            return page_info
        except urllib2.URLError, e:
            if hasattr(e, 'reasion'):
                print u"连接糗事百科失败，错误原因",e.reason
                return None

    # 获取一页的段子列表
    def get_page_items(self, page_index):
        pageinfo = self.get_page(page_index)
        if not pageinfo:
            print u"页面加载失败"
            return None
        pattern = re.compile('h2>(.*?)</h2.*?content">.*?<span>(.*?)</span>.*?number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageinfo)
        page_stories = []
        for item in items:
            page_stories.append([item[0].strip(),item[1].strip(),item[2].strip()])

        return page_stories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                page_stories = self.get_page_items(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index += 1

    # 显示段子信息
    def getOneStroy(self, page_stories, page):
        for story in page_stories:
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
        new_page = 0
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                new_page += 1
                del self.stories[0]
                self.getOneStroy(page_stories, new_page)


spider = QSBK()
spider.start()
