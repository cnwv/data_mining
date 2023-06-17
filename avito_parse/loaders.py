from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
import re
from scrapy import Selector
from urllib.parse import urljoin


def get_full_link(item):
    return urljoin("https://www.instagram.com/p/", item.pop())


class InstaLoader(ItemLoader):
    default_item_class = dict
    post_link_out = get_full_link
    date_out = TakeFirst()
    media_type_out = TakeFirst()
    comments_out = TakeFirst()
