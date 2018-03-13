# -*- coding:utf-8 -*-

import requests
import re
import os

'''
抓取淘女郎（http://mm.taobao.com/json/request_top_list.htm）的信息并将图片保存到本地
根据https://cuiqingcai.com/1001.html修改
'''


class Spider:
    def __init__(self):
        self.baseURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/60.0.3112.113 Safari/537.36'
        }

    def get_page(self, page_num):
        """
        获取整个网页内容
        :param page_num:
        :return:
        """

        geturl = 'https://mm.taobao.com/json/request_top_list.htm?page=' + str(page_num)
        response = requests.get(geturl, headers=self.headers)

        if response.status_code != 200:
            print "链接淘女郎失败，失败原因：" +response.raise_for_status
            return None

        return response.content.decode('gbk')

    # 获取个人经历 todo:完善
    def get_experience(self, url):
        response = requests.get(url, headers=self.headers)
        page = response.content.decode('gbk')
        print page
        pattern = re.compile('<div class="mm-p-info mm-p-experience-info">.*?</h4>(.*?)</div>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1)
        else:
            return None

    def save_img(self, img_url, file_name):
        response = requests.get(img_url, headers=self.headers)
        data = response.content

        with open(file_name, 'wb') as f:
            f.write(data)
            print "正在偷偷地保存了他的一张图片"
            f.close()


    # 保存头像
    def save_icon(self, image_url, name):
        file_name = name + '/icon.jpg'
        self.save_img(image_url, file_name)

    # 保存文本信息
    def save_text_file(self, content, name):
        file_name = name + '.txt'
        f = open(file_name, 'w+')
        print "正在偷偷地保存她的个人信息为：", file_name
        f.write(content.encode('utf-8'))

    def make_dir(self, path):
        path = path.strip()
        is_exists = os.path.exists(path)
        if not is_exists:
            print '偷偷地创建了名字叫做', path, '的文件夹'
            os.makedirs(path)
            return True
        else:
            print "已经创建了", path, "文件夹"
            return False

    # 获取某页内容（返回list）
    def get_page_content(self, page_num):
        page = self.get_page(page_num)
        # re.S它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?'
                             '<a class="lady-name" href="(.*?)" target.*?>(.*?)</a>.*?<strong>(.*?)'
                             '</strong>.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append(('http:'+item[0], 'http:'+item[1], 'http:'+item[2], item[3], item[4], item[5]))

        return contents

    # 保存某也的内容
    def save_page_info(self, page_num):
        contents = self.get_page_content(page_num)

        for item in contents:
            print "发现一位模特，名字叫", item[3], "，芳龄", item[4], "，她在", item[5], "头像地址", item[1]
            print "正在偷偷地保存她的信息"
            print "又意外地发现她的个人资料地址：" , item[2]

            # expericence = self.get_experience(item[2])
            # print expericence

            self.make_dir(item[3])

            # 保存个人简介
            # self.save_text_file(content, item[3])

            # 保存个人头像
            self.save_icon(item[1], item[3])

    def start(self, start, end):
        for i in range(start, end+1):
            print "正在偷偷寻找第", i, "个地方，看看MM在不在"
            self.save_page_info(i)


if __name__ == '__main__':
    spider = Spider()
    # 抓取第一页的数据
    spider.start(1, 1)