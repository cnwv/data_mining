import dotenv
import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
    crawler_setting = Settings()
    crawler_setting.setmodule("avito_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    tags = ['offm1']
    crawler_process.crawl(InstagramSpider,
                          login=os.getenv('INST_LOGIN'),
                          password=os.getenv('INST_PASSWD'),
                          tags=tags
                          )
    crawler_process.start()