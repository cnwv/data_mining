import scrapy


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/accounts/login/"]

    def parse(self, response):
        pass
