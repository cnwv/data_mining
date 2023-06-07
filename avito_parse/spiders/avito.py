import scrapy


# from cookie import cookie

class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["www.avito.ru"]
    start_urls = ["https://www.avito.ru/moskovskaya_oblast_krasnoznamensk/avtomobili?radius=200&searchRadius=200"]
    _xpath_selectors = {'pagination': '',
                        'apartments': ''
                        }
    _xpath_data_selectors = {'title': '',
                             'price': '',
                             'address': '',
                             'parameters': '',
                             'author_link': '',
                             'phone': ''
                             }
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
               }
    cookie = '__zzatw-avito=MDA0dBA=Fz2+aQ==; _ga=GA1.1.1583003459.1685987280; _gcl_au=1.1.119817105.1685987280; _ym_d=1685987280; _ym_isad=1; _ym_uid=1685914974577791184; auth=1; buyer_laas_location=638590; cfidsw-avito=zEs3ppE/JDoca48629MDUPkynTo3nJ4Uw9J0IkQs7CB6uVJVeUWrUJD/Ir+eTlNsCoZUqbnni+nrxlsDwWtcTzsKtNYUx2uO6l27n3k6xfk4C5VOCkQrHu6fkSaY8yJNf2Bw/jPwI8c1Lmny9avyrpOfrb4Nr2kE6asn; f=5.d908952b446ec0dbdc134d8a1938bf884f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c624f9572e6986d0c627e7721a3e5d3cdbb46b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa868884eb6934e9999433be0669ea77fc059c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047d50b96489ab264edc772035eab81f5e1e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa846b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c76ff288cd99dba4666be20ce2cab3354cd0833ebb6c2bf428cd8023375b73629e60a27478f8d196917c7721dca45217b81d92fe4835f7c64b7bfc28c5965fec2e2415097439d404746b8ae4e81acb9fa786047a80c779d5146b8ae4e81acb9fa9bf99c12f484b6092da10fb74cac1eab2da10fb74cac1eabb3ae333f3b35fe91de6c39666ae9b0d77fc79aa341b41fb84eac648cf5c68718; fgsscw-avito=y2A50db9b7bea340a333dfdee8c54fcbd75a1907; ft="PYZzRxxCDdxRVunW9fRuqAMXv9Uo6XHvZog7RJdrgnq42DeHZJWHVzSmNC9BcIWnAVmwmkiWa1XqLFurU8UsTKjXCfSphiKPFCOVDhcQVa7aqUotLwvMvEoKH9LmbigFnAOZmKqFEvJqRX4MfLGxgvESRjtfppRH2T6WePYhGevaeCdXzqcReuj891XIoOAF"; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; gsscw-avito=Oicxy3AayoGZu6PSIvHMVLNCGrqoTsisVJdtIhOOtVApBflhhlAJmyawxG+FxYmsfa9DdSjBejVYul9+jNotENkC83IDdItB+Pis/5jRSz0rfr4uVLIQt2csSMVzXYNXouNz5op76bpbMevICU9cOc//ivLiRe9gvNDonlboI/g0XZBAPt0uvLYf1Bcb5/GRNznUGDJuhEcKrbXYfgQXcvyNJ861S9HMj4vxpLh2GHZwjtHRP8BBoKYZyDGa8Q==; sessid=de93fe75da710b0e98449bf7a5e1bad6.1685987419; tmr_lvid=54c148f84b2f5763958cf83ec400004c; tmr_lvidTS=1685914973946; u=2xxsd7mu.1mvw1tz.16oicho7b8500; luri=moskovskaya_oblast_krasnoznamensk; buyer_location_id=638590; v=1685994018; dfp_group=63; isLegalPerson=0; _ym_visorc=b; sx=H4sIAAAAAAAC%2F1zOTW6DMBAG0Lt4zcLG9jcebhPPYEhFSMKf6kTcvatWVS7w9N7GWddqn7O2WUQzeeud0kUTQ4oXMd3bHKYzaEe5vdaliDyc1hqQMN9nnfu1bnkxjelN55BgKViKZ2MAQJRQGBwRwD3l3rNStCKk%2FCfTsNfrgG0b24c6ydORmfbIwzGl6%2Fc%2FOdng6WyMkFpXQgwgDZxjcT6mVgAOLroSf2V3l%2FLi59fyvKmfiCepl3FGXbHuGx0fZ5znTwAAAP%2F%2FylVqlQ8BAAA%3D; _ga_M29JC28873=GS1.1.1685994019.2.1.1685994038.41.0.0'

    # def start_requests(self):
    #     print(1)
    #     yield scrapy.Request(
    #         url='www.avito.ru',
    #         cookies=cookie,
    #         callback=self.parse
    #     )
    def parse_cookies(self, raw_cookies):
        # parsed cookies
        cookies = {}
        # loop over cookies
        for cookie in raw_cookies.split('; '):
            try:
                # init cookie key
                key = cookie.split('=')[0]

                # init cookie value
                val = cookie.split('=')[1]

                # parse raw cookie string
                cookies[key] = val

            except:
                pass

        return cookies

    # crawler's entry point
    # # def start_requests(self):
    #     print(1)
    #     # make HTTP GET request to "requestbin.com"
    #     yield scrapy.Request(
    #         url=self.start_urls[0],
    #         headers=self.headers,
    #         cookies=self.parse_cookies(self.cookie),
    #         callback=self.parse
    #     )

    def parse(self, response):
        print(1)
        pass
