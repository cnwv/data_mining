from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_parse.spiders.avito import AvitoSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule("avito_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(AvitoSpider)
    crawler_process.start()