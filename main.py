from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.auto import AutoSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule("gb_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(AutoSpider)
    crawler_process.start()

