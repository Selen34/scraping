# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, записывающую собранные вакансии в созданную БД
# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
# 3)*Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
# Доработать функцию, которая будет обновлять старые вакансии.

from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from hashlib import md5
import requests
import pprint
import json
import time
import random
import re


def initDB(name):
    client = MongoClient('localhost', 27017)
    return client[name]


def getHHSearchQuery(str):
    return str.replace(" ",'+')


def getParsedRequest(url):
    uagent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    req = requests.get(url, headers = {'user-agent': uagent})
    return bs(req.content, 'lxml')


def getDataFromItem(item):
    title = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    url = title['href']
    page = getParsedRequest(url)
    rawParams = page.find('script', {'data-name': 'HH/GoogleDfpService'})
    params = json.loads(rawParams['data-params'])
    minSalary = params['vac_salary_from']
    try:
        minSalary = int(minSalary)
    except:
        minSalary = None
    maxSalary = params['vac_salary_to']
    try:
        maxSalary = int(maxSalary)
    except:
        maxSalary = None
    curSalary = params['vac_salary_cur']
    return { 'title': title.text, 'url': url, 'min': minSalary, 'max': maxSalary, 'cur': curSalary, 'site': 'hh.ru' }


def getSJSearchQuery(str):
    return str.replace(" ",'%20')


def dataFromSJItem(item):
    url = item.find('a', {'class': 'icMQ_'})
    url = url['href']
    url = 'https://www.superjob.ru' + url
    title = item.find('div', {'class': '_3mfro'}).text
    page = getParsedRequest(url)
    zp = page.find('span', {'class': '_2Wp8I'})
    minZp = None
    maxZp = None
    cur = 'RUR'
    if zp:
        zp = zp.text.replace('\xa0', '')
        arr = re.findall(r'\d+', zp)
        if len(arr) == 1:
            minZp = arr[0]
        if len(arr) == 2:
            minZp = min(arr)
            maxZp = max(arr)
    return { 'title': title, 'url': url, 'min': minZp, 'max': maxZp, 'cur': cur, 'site': 'superjob.ru'}


def saveOrUpdate(row, client):
    _md5 = md5(str(row).encode()).hexdigest()
    _idh = md5(str(row['url']).encode()).hexdigest()
    collection = row['site'].replace('.', '')
    collection = client[collection]
    exists = collection.find_one({'idh': _idh})
    row['idh'] = _idh
    row['md5'] = _md5
    if exists:
        if exists['md5'] != _md5:
            collection.delete_one({'idh': _idh})
            collection.insert_one(row)
    else:
        collection.insert_one(row)


def searchAndPrint(salary, db, limit=10, asc=True):
    plist = []
    hh = db['hhru']
    sjb = db['superjob.ru']
    ihh = hh.find({'min': { '$gte': salary }}, {'_id': 0, 'idh': 0, 'md5': 0})
    isj = sjb.find({'min': {'$gte': salary}}, {'_id': 0, 'idh': 0, 'md5': 0})
    for item in ihh:
        plist.append(item)
    for item in isj:
        plist.append(item)
    plist = sorted(plist, key=lambda item: item['min'], reverse=not asc)
    print('TOTAL:', len(plist))
    i = 0
    for item in plist:
        if i > limit:
            break
        pprint.pprint(item)
        i += 1


def searchAndSave(inpName, db):
    vacName = getHHSearchQuery(inpName)
    count = 0
    buttonNext = True
    queryString = "https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=" + vacName
    while buttonNext:
        parsed = getParsedRequest(queryString)
        vlist = parsed.find_all('div', {'class': 'vacancy-serp-item'})
        for item in vlist:
            time.sleep(random.randint(1, 2))
            vacData = getDataFromItem(item)
            saveOrUpdate(vacData, db)
            count += 1
        buttonNext = parsed.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if buttonNext:
            queryString = 'https://hh.ru' + buttonNext['href']
        time.sleep(random.randint(1, 2))

    vacName = getSJSearchQuery(inpName)
    sjString = 'https://www.superjob.ru/vacancy/search/?geo%5Bc%5D%5B0%5D=1&keywords=' + vacName
    buttonNext = True
    while buttonNext:
        parsed = getParsedRequest(sjString)
        vlist = parsed.find_all('div', {'class': 'f-test-vacancy-item'})
        for item in vlist:
            time.sleep(random.randint(1, 2))
            tmp = dataFromSJItem(item)
            saveOrUpdate(tmp, db)
            count += 1
        buttonNext = parsed.find('a', {'rel': 'next'})
        if buttonNext:
            urlNext = buttonNext['href']
            sjString = 'https://www.superjob.ru' + urlNext
        time.sleep(random.randint(1, 2))
    print('SAVE OR UPDATED:', count)


if __name__ == '__main__':
    print('UPLOAD VACANCY:')
    inpName = input()
    db = initDB('vacancies')
    searchAndSave(inpName, db)
    print('SEARCH FOR SALARY:')
    salary = input()
    searchAndPrint(int(salary), db)