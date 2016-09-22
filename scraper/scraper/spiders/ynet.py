# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import TalkbackItem, TestItem, ArticleItem


class YnetChannelSpider(CrawlSpider):
    allowed_domains = ["www.ynet.co.il"]

    def __init__(self, max_articles=50, include_talkbacks=True, *args, **kwargs):
        self.max_articles = int(max_articles)
        self.include_talkbacks = True if str(include_talkbacks).lower() == "true" else False
        self.init()
        super(YnetChannelSpider, self).__init__(*args, **kwargs)

    def init(self):
        self.stats_articles_processed = 0
        self._initRules()

    def _initRules(self):
        allowed_urls = ["/articles/.*?.html"]
        if self.include_talkbacks:
            allowed_urls.append("/Ext/App/TalkBack/CdaViewOpenTalkBack/.*?.html")
        self.rules = [
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
    def is_article_in_allowed_channel(self, response):
        return any(
            src.endswith(logo)
            for src in response.xpath("//img/@src").extract()
            for logo in self.__class__.allowed_channel_logos
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
            for x in super(YnetChannelSpider, self)._requests_to_follow(response):
                yield x
        else:
            print "*" * 10, "SHOULD NOT FOLLOW:", response.url

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

    def article_process_limit_reached(self):
        return self.stats_articles_processed >= self.max_articles

    def parse_article(self, response):
        if self.article_process_limit_reached():
            return
        self.stats_articles_processed += 1
        print "*" * 10, "ARTICLE URL:", response.url
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


class NationalNewsSpider(YnetChannelSpider):
    name = "national"
    start_urls = [
        # Index: news -> national
        "http://www.ynet.co.il/home/0,7340,L-188,00.html"
    ]
    allowed_channel_logos = ["national.gif"]


class NationalNewsSpider(YnetChannelSpider):
    name = "politics"
    start_urls = [
        # Index: news -> politics
        "http://www.ynet.co.il/home/0,7340,L-185,00.html"
    ]
    allowed_channel_logos = ["politics.gif"]


class SportsNewsSpider(YnetChannelSpider):
    name = "sports"
    start_urls = [
        "http://www.ynet.co.il/home/0,7340,L-3,00.html"
    ]
    allowed_channel_logos = [
        # bloody hell ynet. this is your sports logo url?
        "short/commerce/2016/links/21/1.png"
    ]


class DatingNewsSpider(YnetChannelSpider):
    name = "dating"
    start_urls = [
        "http://www.ynet.co.il/home/0,7340,L-3925,00.html"
    ]
    allowed_channel_logos = [
        # because every png should be stored differently
        "PicServer4/2016/01/18/6763527/coteret2.png",
        "PicServer/02202003/247088/6.gif",
    ]


class HealthNewsSpider(YnetChannelSpider):
    name = "health"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-1208,00.html"]
    allowed_channel_logos = [
        "PicServer4/2016/04/05/6921963/888.jpg",
        "k_health.gif",
    ]


class EducationNewsSpider(YnetChannelSpider):
    name = "education"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-10511,00.html"]
    allowed_channel_logos = ["limudim1024_(10).jpg"]


class ParentsNewsSpider(YnetChannelSpider):
    name = "parents"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-3052,00.html"]
    allowed_channel_logos = ["kotarot_parents.gif"]


class DigitalNewsSpider(YnetChannelSpider):
    name = "digital"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-544,00.html"]
    allowed_channel_logos = [
        "digital_coteret.jpg",
        "science-_title.jpg",
    ]


class CarsNewsSpider(YnetChannelSpider):
    name = "cars"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-550,00.html"]
    allowed_channel_logos = [
        "k_wheels.gif",
        "308303/koteret.gif",
        "k_newscar.gif",
        "k_ziburi.gif"
    ]


class EconomyNewsSpider(YnetChannelSpider):
    name = "economy"
    start_urls = ["http://www.ynet.co.il/home/0,7340,L-6,00.html"]
    allowed_channel_logos = [
        "kalkala.gif",
        "SHUCK.jpg",
        "6958097/H_title.jpg",
    ]
