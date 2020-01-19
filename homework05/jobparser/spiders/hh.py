# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


def vacancy_parse(response: HtmlResponse):
    title = response.css('h1.header *::text').extract_first()
    salary = response.xpath("//script[@data-name='HH/GoogleDfpService']/@data-params").extract_first()
    yield JobparserItem(title=title, salary=salary, url=response.url)


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true']

    def __init__(self, search):
        super(HhSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text={search}'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancies = response.css('div.vacancy-serp-item__info a.bloko-link::attr(href)').extract()
        for link in vacancies:
            yield response.follow(link, callback=vacancy_parse)
