import scrapy
from ..loaders import HhLoader


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"]
    _xpath_selectors = {'pagination': '//div[contains(@class, "pager")]//a[@class="bloko-button"]/@href',
                        'vacancy': '//div[@id="a11y-main-content"]//div[@class="serp-item"]//h3//a/@href'
                        }
    _xpath_data_selectors = {'title': '//h1[@class="bloko-header-section-1"]/text()',
                             'salary': '//div[@data-qa="vacancy-salary"]/span/text()',
                             'description': "//div[@class='vacancy-section']//text()",
                             'keyskills': '//div[@class="bloko-tag-list"]/div[contains(@class, "bloko-tag")]'
                                          '/span/text()',
                             'company_link': '//div[@class="vacancy-company-details"]/span/a/@href'
                             }
    _xpath_company_selectors = {'company_name': '//div[@class="employer-sidebar-header"]/'
                                                '/h1[@class="bloko-header-1"][1]'
                                                '/span[@class="company-header-title-name"]/text()',
                                'company_website': '//button[@class="bloko-external-link"]/span/text()',
                                'areas_of_work': '//div[@class="employer-sidebar-block"]//p/text()',
                                'company_description': '//div[@class="g-user-content"]//text()'
                                }

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self._xpath_selectors['pagination'], self.parse)
        yield from self._get_follow(response, self._xpath_selectors['vacancy'], self.vacancy_parse)

    def vacancy_parse(self, response):
        loader = HhLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_value('type', 'vacancy')
        for key, xpath in self._xpath_data_selectors.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
        yield from self._get_follow(response, self._xpath_data_selectors['company_link'], self.parse_employer)

    def parse_employer(self, response):
        loader = HhLoader(response=response)
        loader.add_value('hh_url', response.url)
        loader.add_value('type', 'employer')
        for key, xpath in self._xpath_company_selectors.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()

