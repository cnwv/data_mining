# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from .settings import BOT_NAME
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class AvitoParsePipeline:
    def process_item(self, item, spider):
        return item


class InstaMongoPipeline:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        self.db = client[BOT_NAME]

    def process_item(self, item, spider):
        print('записываем')
        self.db[spider.name].insert_one(item)
        print('записано')
        return item


class InstaImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get('photos_url'):
            yield Request(url)

    def item_completed(self, results, item, info):
        if item.get('photos_url', []):
            item['photos_url'] = [itm[1] for itm in results]
        return item
