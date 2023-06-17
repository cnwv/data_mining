import scrapy
import re
from urllib.parse import urljoin
import json
import datetime
from ..loaders import InstaLoader


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/accounts/login/"]
    _login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"

    def __init__(self, login, password, users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.users = users

    def parse(self, response, **kwargs):
        try:
            yield scrapy.FormRequest(
                self._login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password
                },
                headers=self._get_headers(response)
            )
        except ValueError:
            data = response.json()
            # url = f'https://www.instagram.com/api/v1/feed/user/{user}/username/?count=12'
            url = f'https://www.instagram.com/'
            yield response.follow(
                url,
                callback=self.user_parse
            )

    def user_parse(self, response, *args):
        headers = self._get_headers(response)
        for user in self.users:
            url = f'https://www.instagram.com/api/v1/feed/user/{user}/username/?count=12'
            yield response.follow(
                url,
                callback=self._get_data,
                headers=headers,
                cb_kwargs=headers
            )

    def _get_data(self, response, **kwargs):
        posts = response.json()
        for post in posts['items']:
            yield from self._parse_post(post)
        print(1)
        try:
            yield response.follow(
                f"https://www.instagram.com/api/v1/feed/user/{posts['user']['username']}/username/?count=12&max_id={posts['next_max_id']}",
                callback=self._get_data,
                headers=kwargs,
                cb_kwargs=kwargs
            )
        except Exception as e:
            print('fail')




    def _parse_post(self, post):
        media_type = post['media_type']
        photo_urls = []
        if media_type == 1:
            photo_urls.append(post['image_versions2']['candidates'][0]['url'])
        elif media_type == 8:
            for photo in post['carousel_media']:
                photo_urls.append(photo['image_versions2']['candidates'][0]['url'])
        data = {
            'post_link': post['code'],
            'date': datetime.datetime.fromtimestamp(post['taken_at']),
            'photos_url': photo_urls,
            'media_type': media_type,
            'comments': ''
        }
        loader = InstaLoader()
        for k, v in data.items():
            loader.add_value(k, v)
        yield loader.load_item()

    def _get_headers(self, response):
        headers = dict()
        string = response.xpath("//script[contains(text(), 'csrf_token')]/text()").extract_first()
        headers['X-Csrftoken'] = re.search(r'\\"csrf_token\\":\\"([^\\]+)\\"', string).group(1)
        headers['X-Ig-App-Id'] = re.search(r'"X-IG-App-ID":"(\d+)"', string).group(1)
        return headers
