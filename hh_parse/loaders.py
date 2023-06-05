from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from scrapy import Selector
import re
from urllib.parse import urljoin
from base64 import b64decode


def create_text(item):
    result = "".join(item)
    try:
        result.replace('\xa0', '')
    except ValueError:
        result = None
    return result


def get_description(item):
    cleaned_text = "".join(item)
    return cleaned_text


def create_company_url(item):
    return urljoin("https://hh.ru/", item.pop())


class HhLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = create_text
    description_out = get_description
    company_link_in = create_company_url
    company_link_out = TakeFirst()

    hh_url_out = TakeFirst()
    company_name_out = create_text
    company_website_out = TakeFirst()
    company_description_out = get_description
