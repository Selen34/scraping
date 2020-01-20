# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru']

    def __init__(self, section):
        super(LeroySpider, self).__init__()
        self.start_urls = [
            f'https://leroymerlin.ru/catalogue/{section}'
        ]

    def parse(self, response):
        item_links = response.css('div.product-name a::attr(href)').extract()
        for link in item_links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_css('title', 'h1.header-2::text')
        loader.add_value('url', response.url)
        loader.add_value('_id', response.url)
        loader.add_css('prop_titles', 'div.characteristics-property-title')
        loader.add_css('prop_values', 'div.characteristics-property-value')
        loader.add_xpath('pics', "//picture[@slot='pictures']")
        yield loader.load_item()

