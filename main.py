import time

import requests
import json
from pathlib import Path


class ParseDetMir:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    params = {
        'page': 1
    }
    next_page = True

    def __init__(self, save_path: Path, url):
        self.save_path = save_path
        self.url = url

    def run(self):
        for product in self._parse():
            file_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, file_path)

    def _parse(self):
        while self.next_page:
            time.sleep(0.1)
            response = self._get_response()
            data = response.json()
            self.params['page'] += 1
            if self.params['page'] > data['products']['last_page']:
                self.next_page = False
            for product in data['products']['data']:
                print(product['name']) #TODO После создания второго экземпляра класса товары не отображаются.
                yield product


    def _get_response(self):
        while True:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                return response
            time.sleep(2)

    def _save(self, product, file_path):
        file_path.write_text(json.dumps(product))


class Get_category:
    url = 'https://ispace.ge/api/catalog/categories'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    next_page = True

    def run(self):
        for category in self._parse():
            path = self.mkdir(str(category['id']))
            category_url = 'https://ispace.ge/api/apr/catalog/products/category' + '/' + category['url']
            print(f"Creating ParseDetMir instance for URL: {category_url}")
            category = ParseDetMir(path, category_url)
            print(f"Created instance of ParseDetMir with id {id(category)}")
            category.run()
    def _parse(self):
        response = self._get_response()
        data = response.json()
        for i in data:
            time.sleep(0.1)
            for category in i['children']:
                yield category

    def _get_response(self):
        while True:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(2)

    def mkdir(self, dir):
        save_path_category = Path("products").joinpath(dir)
        if not save_path_category.exists():
            save_path_category.mkdir()
        return save_path_category


def get_save_path(dir):
    save_path = Path(__file__).parent.joinpath(dir)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    get_save_path("products")
    parser = Get_category()
    parser.run()
