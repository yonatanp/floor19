# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pformat

from scraper.items import TestItem, TalkbackItem, ArticleItem


class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item

import json
import codecs
from collections import OrderedDict


utfopen = lambda path, mode: codecs.open(path, mode, encoding="utf-8")

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.talkback_file = utfopen('talkbacks.json', 'w')
        self.article_file = utfopen('articles.json', 'w')
        self.test_file = utfopen('test_output.json', 'w')

    def process_item(self, item, spider):
        json_line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"

        if isinstance(item, TestItem):
            # escape for TestItem
            self.test_file.write(json_line)
            return None

        if isinstance(item, TalkbackItem):
            self.output_talkback(json_line)
        if isinstance(item, ArticleItem):
            self.output_article(json_line)

        return item

    def output_talkback(self, json_line):
        self.talkback_file.write(json_line)

    def output_article(self, json_line):
        self.article_file.write(json_line)

    def close_spider(self, spider):
        self.talkback_file.close()
        self.article_file.close()
        self.test_file.close()


class PrintTalkbackTexts(object):
    def __init__(self):
        open("all_talkback_lines.txt", "w").close()
    def process_item(self, item, spider):
        if isinstance(item, TalkbackItem):
            raise 3
            utfopen("all_talkback_lines.txt", "a").write(item.title_text + "\n")
        return item


class DebugPrettyPrint(object):
    def __init__(self):
        open("debug_pretty_print.txt", "w").close()
    def process_item(self, item, spider):
        print >> utfopen("debug_pretty_print.txt", "a"), pformat(item)
