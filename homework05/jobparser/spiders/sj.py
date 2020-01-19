# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


def vacancy_parse(response: HtmlResponse):
    title = response.css('h1._3mfro *::text').extract_first()
    salary = response.css('div._3MVeX span._2Wp8I *::text').extract()
    yield JobparserItem(title=title, salary=salary, url=response.url)


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?geo%5Bc%5D%5B0%5D=1']

    def __init__(self, search):
        super(SjSpider, self).__init__()
        self.start_urls = [
            f'https://www.superjob.ru/vacancy/search/?geo%5Bc%5D%5B0%5D=1&keywords={search}'
        ]

    def parse(self, response):
        next_page = response.css('a.f-test-button-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancies = response.css('div.f-test-vacancy-item a._1QIBo::attr(href)').extract()
        for link in vacancies:
            yield response.follow(link, callback=vacancy_parse)


