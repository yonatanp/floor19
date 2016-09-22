# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from scraper.items import TalkbackItem, TestItem, ArticleItem

MAX_ARTICLES = 500
INCLUDE_TALKBACKS = True # False


class TalkbackSpider(CrawlSpider):
    name = "talkback"
    allowed_domains = ["www.ynet.co.il"]
    start_urls = [
        # Yair Lapid
        #"http://www.ynet.co.il/articles/0,7340,L-4858313,00.html",
        # [TB] "http://www.ynet.co.il/Ext/App/TalkBack/CdaViewOpenTalkBack/0,11382,L-4858313,00.html",

        # Zoabi
        # "http://www.ynet.co.il/Ext/App/TalkBack/CdaViewOpenTalkBack/0,11382,L-3898005,00.html",

        # Index: news -> national
        "http://www.ynet.co.il/home/0,7340,L-188,00.html"
    ]

    allowed_urls = ["/articles/.*?.html"]
    if INCLUDE_TALKBACKS:
        allowed_urls.append("/Ext/App/TalkBack/CdaViewOpenTalkBack/.*?.html")

    rules = [
        Rule(
            LinkExtractor(
                allow=allowed_urls,
                deny=[
                    # "RSS Updates"
                    "/articles/0,7340,L-3369891,00.html",
                ],
                # restrict_xpaths=['//a[@class="index"]']
            ),
            callback="parse_items",
            follow=True,
        )
    ]

    # Maybe not the best way, but I do not want to harvest links from pages that are outside National limits
    ALLOWED_CHANNEL_LOGOS = ["national.gif"]
    def is_article_in_allowed_channel(self, response):
        return any(
            src.endswith(logo)
            for src in response.xpath("//img/@src").extract()
            for logo in self.ALLOWED_CHANNEL_LOGOS
        )

    def _requests_to_follow(self, response):
        should_follow = True
        if "/articles/" in response.url:
            # we don't follow articles that are outside allowed channels
            if not self.is_article_in_allowed_channel(response):
                should_follow = False
            # we don't follow articles after we've reached our goal
            if self.article_process_limit_reached():
                should_follow = False
        if should_follow:
            for x in super(TalkbackSpider, self)._requests_to_follow(response):
                yield x
        else:
            print "*"*10, "SHOULD NOT FOLLOW:", response.url

    def parse_items(self, response):
        if "Ext/App/TalkBack/CdaViewOpenTalkBack" in response.url:
            for x in self.parse_talkbacks(response):
                yield x
        if "/articles/" in response.url:
            for x in self.parse_article(response):
                yield x

    # this is important because our first page might be an interesting one; we parse all in the same way.
    def parse_start_url(self, response):
        return [x for x in self.parse_items(response)]

    # TODO: this is a hack
    stats_articles_processed = 0
    MAX_ARTICLES_TO_PROCESS = MAX_ARTICLES
    def article_process_limit_reached(self):
        return self.stats_articles_processed >= self.MAX_ARTICLES_TO_PROCESS

    def parse_article(self, response):
        if self.article_process_limit_reached():
            return
        self.stats_articles_processed += 1
        print "*"*10, "URL:", response.url
        print >> open("urls_temp.txt", "a"), response.url

        article_texts = []
        for p_text in response.xpath("//article").xpath(".//p/text()").extract():
            p_text = p_text.strip()
            if p_text:
                article_texts.append(p_text)

        header_title = response.css("div.art_header_title").xpath("text()").extract_first()
        if header_title is None:
            header_title = ""
        header_title = header_title.strip()

        article_id = response.url.split("/articles/")[1].strip()

        if article_texts:
            yield ArticleItem(
                full_text="\n".join(article_texts),
                header_title=header_title,
                article_id=article_id,
            )

    def parse_talkbacks(self, response):
        hxs = Selector(response)
        html_title = hxs.xpath("//title")
        talkback_title_lines = hxs.xpath("//div[@id='titleDiv']")  # titles
        yield TestItem(
            field=html_title[0].xpath("text()").extract(),
            url=response.url,
        )

        for talkback_title_line in talkback_title_lines:
            full_line_text = talkback_title_line.xpath("text()").extract_first()
            if "PARSE UGLY INDEX SYNTAX":
                # format: "###. bla bla bla" except that the "space" is actually "\xa0" (HEBREW.)
                (index, title_text) = full_line_text.split(".", 1)
                title_text = title_text.strip()
            article_id = response.css("a.bluelink").xpath("./@href").extract_first().split("/articles/")[1]
            yield TalkbackItem(
                title_text=title_text,
                index=index,
                article_id=article_id,
            )
