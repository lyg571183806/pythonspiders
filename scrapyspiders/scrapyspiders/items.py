# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(url_object_id, title, url, create_date, fav_nums, front_image_url, front_image_path,
            praise_nums, comment_nums, category, tags, content, create_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """

        fron_image_url = ""
        # content = remove_tags(self["content"])
        create_at = datetime.datetime.now().timestamp()
        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self['url_object_id'], self["title"], self["url"], self["create_date"], self["fav_nums"],
                  fron_image_url, self["front_image_path"], self["praise_nums"], self["comment_nums"], self['category'],
                  self["tags"], self["content"], str(create_at))
        return insert_sql, params