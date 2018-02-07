# -*- coding: utf-8 -*-
__author__ = 'yunshu'

from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 使用scrapy crawl jobbole调用scrapy爬取
# execute(['scrapy', 'crawl', 'lagou'])
execute(['scrapy', 'crawl', 'jobbole'])