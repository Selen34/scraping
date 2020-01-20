# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from youlaparser.items import YoulaparserItem


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = ['http://youla.ru/']

    def __init__(self, section):
        super(YoulaSpider, self).__init__()
        self.start_urls = [
            f'https://youla.ru/moskva/{section}'
        ]

    def parse(self, response: HtmlResponse):
        item_links = response.css('li.product_item a::attr(href)').extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        pass
