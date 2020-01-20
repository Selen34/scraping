from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from youlaparser import settings
from youlaparser.spiders.youla import YoulaSpider


if __name__ == '__main__':
    # foto-video etc
    search = 'zhenskaya-odezhda'
    print('UPLOAD SECTION:', search)
    # search = input()
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(YoulaSpider, section=search)
    process.start()
    print('DONE')
