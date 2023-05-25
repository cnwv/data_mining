import scrapy
import re
from pymongo import MongoClient
from database import Database


class AutoSpider(scrapy.Spider):
    name = "auto"
    allowed_domains = ["shinyprofi.ru"]
    start_urls = ["https://www.shinyprofi.ru/shiny/"]
    db = Database()

    def _get_follow(self, response, selector_str, callback):
        for itm in response.css(selector_str):
            url = itm.attrib["href"]
            yield response.follow(url, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response,
            '.wheels_manufacturers_list .wheels_manufacturer_td a.no-border',
            self.brand_parse
        )

    def brand_parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response,
            '.paging .pages a',
            self.brand_parse
        )
        yield from self._get_follow(
            response,
            '.wheels_list .wheels_td .wheels_name a',
            self.car_parse
        )

    def car_parse(self, response):
        data = {
            'brand': response.css('.breadcrumbs ul li span::text')[4].get(),
            'model': re.sub(r'^\w+\s*', '', response.css('.breadcrumbs ul li::text').get()),
            'url': response.url,
            'img': response.urljoin(response.css('.wheels-open-left a::attr(href)').get())
        }
        self.db.insert_data(data)


