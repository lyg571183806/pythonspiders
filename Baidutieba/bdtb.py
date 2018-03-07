# -*- coding:utf-8 -*-
__author__ = 'yunshu'

import urllib2
import re


# 爬取百度贴吧帖子
class Tool:
    # 去除img标签以及7位长空格
    removeImg = re.compile("<img.*?>| {7}")
    # 去除<br>标签
    removeBR = re.compile('<br><br>|<br>')
    # 去除a链接标签
    removeA = re.compile('<a href=.*?>|</a>')

    def replace(self, replaceStr):
        replaceStr = re.sub(self.removeImg, "", replaceStr)
        replaceStr = re.sub(self.removeBR, "\n", replaceStr)
        replaceStr = re.sub(self.removeA, "", replaceStr)

        return replaceStr.strip()


class BDTB:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    # seeLZ:只看楼主，floorFlag:记录楼层
    def __init__(self, baseUrl, seeLZ, floorFlag):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.defaultTitle = '百度贴吧'
        self.floorFlag = floorFlag
        self.floor = 1

    # 传入页码，获取页面内容
    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)

            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print
                "连接百度贴吧失败，错误原因", e.reason
                return None

    def getTitile(self, page):
        # re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符。
        # h3的情况：https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1
        # h1的情况：http://tieba.baidu.com/p/5326642454?see_lz=1&pn=1
        pattern = re.compile('<(h3|h1).*?>(.*?)</h', re.S)
        result = re.search(pattern, page)
        if (result):
            return result.group(2).strip()
        else:
            return None

    # 获取帖子页数
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num".*?<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if (result):
            return result.group(1).strip()
        else:
            return None

    # 获取每一层的帖子内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = self.tool.replace(item)
            if content != '':
                contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')

    def writeData(self, contents):
        floor = 1
        for item in contents:
            if self.floorFlag == '1':
                floorstr = "\n%d ------------------------------------------------\n" % (self.floor)
                self.file.write(floorstr)
                self.floor += 1
            self.file.write(item)

    def start(self):
        indexPage = self.getPage(1)

        if indexPage == None:
            return
        pageNum = self.getPageNum(indexPage)

        if (pageNum == None):
            print
            "URL已失效，请重试"
            return

        title = self.getTitile(indexPage)
        self.setFileTitle(title)
        print
        "帖子标题：" + str(title)
        print
        "该帖子共有：" + str(pageNum) + "页"
        try:
            for i in range(1, int(pageNum) + 1):
                print
                "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print
            "写入文件异常，原因：" + e.message
        finally:
            print
            "写入任务完成"


print
"请输入帖子代号"
baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input('http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorFlag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
dbtb = BDTB(baseUrl, seeLZ, floorFlag)
dbtb.start()