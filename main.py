import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
    crawler_setting = Settings()
    crawler_setting.setmodule("avito_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(InstagramSpider)
    crawler_process.start()