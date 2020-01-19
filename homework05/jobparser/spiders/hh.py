# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancies = response.css('div.vacancy-serp-item__info a.bloko-link::attr(href)').extract()
        for link in vacancies:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(selfs, respose: HtmlResponse):
        title = respose.css('h1.header *::text').extract_first()
        salary = respose.xpath("//script[@data-name='HH/GoogleDfpService']/@data-params").extract_first()
        yield JobparserItem(title=title, salary=salary, url=respose.url)
