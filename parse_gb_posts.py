import time
import typing

from urllib.parse import urljoin
import requests
import bs4
from pymongo import MongoClient
import datetime


class GBlogParse:

    def __init__(self, start_url, collection):
        self.time = time.time()
        self.start_url = start_url
        self.collection = collection
        self.done_urls = set()
        self.tasks = []
        start_task = self.get_task(self.start_url, self.parse_feed)
        self.tasks.append(start_task)
        self.done_urls.add(self.start_url)

    def _get_response(self, url, *args, **kwargs):
        if self.time + 0.1 < time.time():
            time.sleep(0.1)
        response = requests.get(url, *args, **kwargs)
        self.time = time.time()
        print(url)
        return response

    def _get_soup(self, url, *args, **kwargs):
        soup = bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")
        return soup

    def get_task(self, url: str, callback: typing.Callable) -> typing.Callable:
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        if url in self.done_urls:
            return lambda *_, **__: None
        self.done_urls.add(url)
        return task

    def task_creator(self, links, callback):
        for link in links:
            task = self.get_task(link, callback)
            self.tasks.append(task)

    def parse_feed(self, url, soup):
        ul_pagination = soup.find("ul", attrs={"class": "gb__pagination"})
        links = set(urljoin(url, itm.attrs.get('href'))
                    for itm in ul_pagination.find_all('a') if itm.attrs.get('href')
                    )
        self.task_creator(links, self.parse_feed)
        post_wrapper = soup.find("div", attrs={"class": "post-items-wrapper"})
        a_links = set(urljoin(url, itm.attrs.get("href"))
                      for itm in post_wrapper.find_all("a", attrs={"class": "post-item__title"}) if
                      itm.attrs.get("href")
                      )
        self.task_creator(a_links, self.parse_post)

    def insert_data(self, data, type):
        self.collection[type].insert_one(data)

    def get_comments(self, url):
        data = []
        response = self._get_response(url).json()
        if response == []:
            data = 'None'
            return data
        else:
            for comment in response:
                dict = {'name': comment['comment']['user']['full_name'],
                        'comment': comment['comment']['body']}
                data.append(dict)
            return data

    def parse_post(self, url, soup):
        div = soup.find('div', attrs={'class': 'blog-wrap'})
        if div is not None:
            data = {'format': 'blog', 'url': url, 'head': soup.find("h1").text}
            date_soup = soup.find('div', attrs={'class': 'header-date'}).text
            data['date'] = datetime.datetime.strptime(date_soup, '%d.%m.%Y')
            author_div = list(soup.find('div', attrs={'class': 'author-box__author'}).children)
            data['author_link'] = author_div[1]['href']
            data['author_name'] = bs4.BeautifulSoup(str(author_div[1]), 'html.parser').text.strip()
            self.insert_data(data, 'gb_blogs')
        else:
            author_link = soup.find('a', attrs={'class': 'posts-user-info'})
            commentable_id = soup.find("comments")["commentable-id"]
            comments = self.get_comments(f'https://gb.ru/api/v2/comments?commentable_type=Post&'
                                         f'commentable_id={commentable_id}&order=desc')
            data = {'format': 'post', 'url': url, 'head': soup.find("h1").text,
                    'date': datetime.datetime.fromisoformat(
                        soup.find('time', attrs={"class": 'text-md text-muted m-r-md'}).get('datetime')),
                    'author_name': soup.find('div', attrs={'class': 'text-lg text-dark'}).text,
                    'author_link': urljoin(self.start_url, author_link.get('href')),
                    'comments': comments
                    }
            self.insert_data(data, 'gb_posts')

    def run(self):
        for task in self.tasks:
            task_result = task()


if __name__ == '__main__':
    db = MongoClient()["gb_parse_09_20"]
    parser = GBlogParse("https://gb.ru/posts", db)
    parser.run()

