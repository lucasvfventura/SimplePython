import scrapy


class LondonDrugsSpider(scrapy.Spider):
    name = "londondrugs"

    search_term = ""

    def start_requests(self):
        """
        Setup initial url request
        """
        self.search_term = getattr(self, 'search', None)
        if self.search_term is not None:
            search_url = 'http://www.londondrugs.com/on/demandware.store/Sites-LondonDrugs-Site/default/Search-Show?q={0}%27&simplesearch=Go'.format(
                self.search_term)
            yield scrapy.Request(search_url, self.parse)
        else:
            print("Please specify the search term with the parameter search, i.e, -a search=search_term")
            return

    def parse(self, response: scrapy.http.TextResponse):
        """
        Parse the search page. Looks for item specific page and the next page in the search results
        """
        if response.status in [301, 302, 503] and 'Location' in response.headers:
            yield scrapy.Request(response.headers['location'], callback=self.parse)
            return

        for item in response.xpath('//p[@class="productimage"]//a/@href').extract():
            item_url = response.urljoin(item)
            yield scrapy.Request(item_url, callback=self.parse_item)

        next_page = response.xpath('//div[@class="pagination"]//a[@class="pagenext"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        """
        Parse the page describing the item
        """

        def get_data(xpath):
            """
            Return the strip text of the given xpath
            """
            element = response.xpath(xpath).extract_first()
            if element is not None:
                return element.strip()
            else:
                return None

        price_text = get_data('//div[@itemprop="price"]/text()')

        yield {
            'search': self.search_term,
            'url': response.url,
            'source': self.name,
            'product': get_data('//h1[@class="productname"]/text()'),
            'brand': get_data('//h2[@itemprop="brand"]/text()'),
            'currency': 'CDN$',
            'price': float(price_text[1:].replace(',',''))
        }
