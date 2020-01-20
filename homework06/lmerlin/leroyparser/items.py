# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from lxml import html
from hashlib import md5
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def extract_pic(value):
    return html.fromstring(value).xpath(".//source/@data-origin")[0]


def get_id(value):
    return md5(str(value).encode()).hexdigest()


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field(input_processor=Compose(get_id), output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    prop_titles = scrapy.Field()
    prop_values = scrapy.Field()
    pics = scrapy.Field(input_processor=MapCompose(extract_pic))


