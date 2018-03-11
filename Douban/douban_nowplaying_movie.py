# -*- coding:utf-8 -*-
__author__ = 'yunshu'

'''
抓取豆瓣热映电影 https://movie.douban.com/cinema/nowplaying
在python 2.7下测试通过
在python 3下运行会有点问题：
1. 出现"no moudle named 'markupbase'"错误，
解决方法：将所有的 markupbase 改为 _markupbase 即可。原因为markupbase是py2库的，_markupbase是py3库的。
2. from urllib import urlretrieve => from urllib import urlretrieve 
'''
from urllib import urlretrieve
import requests
import os
from HTMLParser import HTMLParser

# HtmlParser，顾名思义，是解析Html的一个工具。python自带的。
# 一、常用属性和方法介绍
# 　　HtmlParser是一个类，在使用时一般继承它然后重载它的方法，来达到解析出需要的数据的目的。
#
# 　 1. 常用属性:lasttag，保存上一个解析的标签名，是字符串。
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
        self.in_movies = False

    def handle_starttag(self, tag, attrs):
        def _attr(attrs, attrname):
            for v in attrs:
                if v[0] == attrname:
                    return v[1]
            return None

        if tag == 'li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-score') and _attr(attrs, 'data-region') \
                and _attr(attrs, 'data-actors') and _attr(attrs, 'data-category') == 'nowplaying':
            movie = {
                'title': _attr(attrs, 'data-title'),
                'score': _attr(attrs, 'data-score'),
                'region': _attr(attrs, 'data-region'),
                'actors': _attr(attrs, 'data-actors'),
            }
            self.movies.append(movie)
            self.in_movies = True
            print('%(title)s|%(score)s|%(region)s|%(actors)s|' % movie)
        if tag == 'img' and self.in_movies == True:
            movie = self.movies[len(self.movies)-1]
            movie['img_url'] = _attr(attrs, 'src')
            download_movie_cover_img(movie)


def download_movie_cover_img(movie):
    img_url = movie['img_url']
    file_name = img_url.split('/')[-1]
    file_ext = os.path.splitext(file_name)[1]
    urlretrieve(img_url, 'imgs/'+movie['title']+file_ext)


def get_movies(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    url = 'https://movie.douban.com/cinema/nowplaying/'+city
    response = requests.get(url, headers=headers)
    parse = MovieParser()
    parse.feed(response.content)
    response.close()
    return parse.movies


if __name__ == '__main__':
    city = ''
    while city == '':
        city = raw_input('please enter city:')
        if city != '':
            movies = get_movies(city)

            import json
            # separators元祖第一个元素为项分割符，第二个为每项里的元素分隔符
            print('%s' % json.dumps(movies, indent=4, separators=(',', ':')))