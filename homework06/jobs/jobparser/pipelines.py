# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from hashlib import md5
import json
import re


def get_hh_salary(salary):
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


def get_sj_salary(salary):
    min_zp = None
    max_zp = None
    if salary:
        tmp = "".join(salary)
        tmp = tmp.replace('\xa0', '')
        arr = re.findall(r'\d+', tmp)
        if len(arr) == 1:
            min_zp = arr[0]
        if len(arr) == 2:
            min_zp = min(arr)
            max_zp = max(arr)
    return {'min': min_zp, 'max': max_zp, 'cur': 'RUR'}


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.scrapyDB
        self.collection = self.db['jobs']

    def process_item(self, item, spider):
        if spider.name == 'hh':
            salary = get_hh_salary(item['salary'])
        else:
            salary = get_sj_salary(item['salary'])
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
        pass
        return item
