# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from hashlib import md5
import json

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.scrapyDB
        self.collection = self.db['jobs']

    def process_item(self, item, spider):
        print(item, spider)
        print(spider.name)
        print(item['title'], item['salary'])
        salary = self.getHHSalary(item['salary'])
        row = {
            'title': item['title'],
            'site': spider.name,
            'url': item['url'],
            'min': salary['min'],
            'max': salary['max'],
            'cur': salary['cur']
        }
        url_md5 = md5(str(row['url']).encode()).hexdigest()
        self.collection.update_one({'_id': url_md5}, {'$set': row}, upsert=True)
        print(row)
        pass
        return item

    def getHHSalary(self, salary):
        params = json.loads(salary)
        min_salary = params['vac_salary_from']
        try:
            min_salary = int(min_salary)
        except:
            min_salary = None
        max_salary = params['vac_salary_to']
        try:
            max_salary = int(max_salary)
        except:
            max_salary = None
        cur_salary = params['vac_salary_cur']
        return {'min': min_salary, 'max': max_salary, 'cur': cur_salary}
