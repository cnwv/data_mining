import time
import typing

from urllib.parse import urljoin
import requests
import bs4
# from pymongo import MongoClient
import datetime
from database.database import Database


class GBlogParse:

    def __init__(self, start_url, db):
        self.time = time.time()
        self.start_url = start_url
        self.db = db
        self.done_urls = set()
        self.tasks = []
        start_task = self.get_task(self.start_url, self.parse_feed)
        self.tasks.append(start_task)
        self.done_urls.add(self.start_url)

    def run(self):
        for task in self.tasks:
            task_result = task()

    def _get_response(self, url, *args, **kwargs):
        if self.time + 0.1 < time.time():
            time.sleep(0.1)
        response = requests.get(url, *args, **kwargs)
        if response.status_code == 404:
            pass
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

    def save(self, data):
        self.db.add_data(data)

    def get_comments(self, url):
        comments = []
        response = self._get_response(url).json()
        for comment in response:
            comments.append(self.parse_comment(comment))
        return comments

    def parse_comment(self, comment):
        commentator = comment.get('comment').get('user').get('full_name')
        text = comment.get('comment').get('body')
        include = comment.get('comment').get('children')
        if include:
            for child in include:
                include = self.parse_comment(child)

        return {'author': commentator, 'text': text, 'include': include}

    def parse_post(self, url, soup):

        div = soup.find('div', attrs={'class': 'blog-wrap'})
        if div is not None:
            return
        else:
            author_link = soup.find('a', attrs={'class': 'posts-user-info'})
            id = soup.find("comments")["commentable-id"]
            comments = self.get_comments(f'https://gb.ru/api/v2/comments?commentable_type=Post&'
                                         f'commentable_id={id}&order=desc')
            data = {'post_data': {
                'id': id,
                'title': soup.find("h1").text,
                # 'date': datetime.datetime.fromisoformat(soup.find('time', attrs={"class": 'text-md text-muted m-r-md'}).get('datetime')),
                'url': url
            }, 'author_data': {
                'id':
                    soup.find("div", attrs={"itemprop": "author"}).parent.attrs.get("href").split("/")[-1],
                'name': soup.find('div', attrs={'class': 'text-lg text-dark'}).text,
                'url': urljoin(self.start_url, soup.find('a', attrs={'class': 'posts-user-info'}).get('href'))
            },
                'tags_data': [
                    {"name": tag.text}
                    for tag in soup.find_all("a", attrs={"class": "small"})
                ],
                'comments_data': comments
            }
            self.save(data)


if __name__ == '__main__':
    # db = MongoClient()["gb_parse_09_20"]
    db = Database("sqlite:///gb_blog.db")
    parser = GBlogParse("https://gb.ru/posts", db)
    parser.run()
