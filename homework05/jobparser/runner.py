from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hh import HhSpider
from jobparser.spiders.sj import SjSpider


def get_sj_query(string: str):
    return string.replace(" ", '%20')


def get_hh_query(string: str):
    return string.replace(" ", '+')


if __name__ == '__main__':
    print('UPLOAD VACANCY:')
    search = input()
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider, search=get_hh_query(search))
    process.crawl(SjSpider, search=get_sj_query(search))
    process.start()
    print('DONE')
