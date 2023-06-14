import scrapy
import re
import json


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/accounts/login/"]
    _login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    _tag_path = '/explore/tags/'

    def __init__(self, login, password, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response):
        try:
            csrf_data = self._get_csrf_token(response)
            yield scrapy.FormRequest(
                self._login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password
                },
                headers={
                    'X-Csrftoken': csrf_data
                }
            )
        except ValueError:
            data = response.json()
            for tag in self.tags:
                yield response.follow(
                    f'{self._tag_path}{tag}/',
                    callback=self.tag_page_parse)

    def tag_page_parse(self, response):
        print(1)

    def _get_csrf_token(self, response):
        script = response.xpath("//script[contains(text(), 'csrf_token')]/text()").extract_first()
        match = re.search(r'\\"csrf_token\\":\\"([^\\]+)\\"', script)
        csrf_token = match.group(1)
        return csrf_token
