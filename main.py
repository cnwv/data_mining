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
    users = ['a.lshim']
    crawler_process.crawl(InstagramSpider,
                          login=os.getenv('INST_LOGIN'),
                          password=os.getenv('INST_PASSWD'),
                          users=users
                          )
    crawler_process.start()