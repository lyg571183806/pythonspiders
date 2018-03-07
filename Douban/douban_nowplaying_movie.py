# -*- coding:utf-8 -*-
__author__ = 'yunshu'

import requests
from HTMLParser import HTMLParser

# HtmlParser，顾名思义，是解析Html的一个工具。python自带的。
# 一、常用属性和方法介绍
# 　　HtmlParser是一个类，在使用时一般继承它然后重载它的方法，来达到解析出需要的数据的目的。
#
# 　1.常用属性:lasttag，保存上一个解析的标签名，是字符串。
#
# 　 2. 常用方法：　
# 　 handle_starttag(tag, attrs) ，处理开始标签，比如 < div >；这里的attrs获取到的是属性列表，属性以元组的方式展示
# 　 handle_endtag(tag) ，处理结束标签, 比如 < / div >
# 　 handle_startendtag(tag, attrs) ，处理自己结束的标签，如 < img / >
# 　 handle_data(data) ，处理数据，标签之间的文本
# 　 handle_comment(data) ，处理注释， < !-- -->之间的文本


class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []

    def handle_starttag(self, tag, attrs):
        def _attr(attrs, attrname):
            for v in attrs:
                if v[0] == attrname:
                    return v[1]
            return None

        if tag == 'li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-score') and _attr(attrs, 'data-region') \
                and _attr(attrs, 'data-actors'):
            movie = {
                'title': _attr(attrs, 'data-title'),
                'score': _attr(attrs, 'data-score'),
                'region': _attr(attrs, 'data-region'),
                'actors': _attr(attrs, 'data-actors'),
            }
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(region)s|%(actors)s|' % movie)


def get_movies(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    url = 'https://movie.douban.com/cinema/nowplaying/'+city
    response = requests.get(url, headers=headers)
    parse = MovieParser()
    parse.feed(response.content)
    response.close()
    return parse.movies


if __name__ == '__main__':
    movies = get_movies('shenzhen')

    import json
    print('%s' % json.dumps(movies, indent=4, separators=(',', ':')))