# -*- coding:utf-8 -*-
import os
import requests
import re
import codecs
from lxml import etree


def save_file(save_path, filename, lists):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".txt"
    with codecs.open(path, "w+", "utf-8") as fp:
        for s in lists:
            fp.write("%s\t\t%s\n" % (s[0], s[1]))
    fp.close()


def get_categories(content):
    pattern = r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>'
    return re.findall(pattern, content, re.S)


def get_news(new_page):
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))

    #返回新闻标题和新闻链接的一个元祖
    return zip(new_items, new_urls)


def spider(url):
    i = 0
    print("downloading ", url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers).content
    page_content = response.decode('gbk');

    categories = get_categories(page_content)
    save_path = u"网易新闻抓取"
    filename = str(i)+"_"+u"新闻排行榜"
    save_file(save_path, filename, categories)

    i += 1
    for category, url in categories:
        print("downloading ", url)
        page_content = requests.get(url).content.decode('gbk')
        news = get_news(page_content)
        filename = str(i)+"_"+category
        save_file(save_path, filename, news)
        i += 1


if __name__ == '__main__':
    print("start")
    start_url = "http://news.163.com/rank/"
    spider(start_url)
    print("end")
