from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hh_parse.spiders.hh import HhSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule("hh_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(HhSpider)
    crawler_process.start()

