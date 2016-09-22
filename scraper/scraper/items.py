# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TalkbackItem(scrapy.Item):
    title_text = scrapy.Field()
    index = scrapy.Field()
    article_id = scrapy.Field()

class ArticleItem(scrapy.Item):
    full_text = scrapy.Field()
    header_title = scrapy.Field()
    article_id = scrapy.Field()

class TestItem(scrapy.Item):
    field = scrapy.Field()
    url = scrapy.Field()
