# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from lxml import html


class LeroyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.scrapyDB
        self.collection = self.db['leroymerlin']

    def process_item(self, item, spider):
        obj = {'title': item['title'], 'pics': item['pics'], 'url': item['url']}
        titles = []
        values = []
        for t in item['prop_titles']:
            titles.append(html.fromstring(t).xpath('.//text()')[0].strip())
        for t in item['prop_values']:
            values.append(html.fromstring(t).xpath('.//text()')[0].strip())
        tmp = []
        for i in range(len(titles)):
            tmp.append({'name': titles[i], 'value': values[i]})
        obj['properties'] = tmp
        self.collection.update_one({'_id': item['_id']}, {'$set': obj}, upsert=True)
        return item


class LeroyImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pics']:
            for src in item['pics']:
                try:
                    yield scrapy.Request(src)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['pics'] = [obj[1] for obj in results if obj[0]]
        return item

