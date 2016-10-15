import scrapy

class AmazonSpider(scrapy.Spider):
    name = "amazon-notebook"

    def start_requests(self):
        search_url2 = 'https://www.amazon.ca/notebook/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3Anotebook'
        search_term = getattr(self, 'search', None)
        if search_term is not None:
            search_url = 'https://www.amazon.ca/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={0}&rh=i%3Aaps%2Ck%3A{0}'.format(search_term)
            yield scrapy.Request(search_url2, self.parse)
        else:
            print("Please specify the search term with the parameter search, i.e, -a search=search_term")
            return

    def parse(self, response):
        """
        Parse the search page. Looks for item specific page and the next page in the search results
        """
        if response.status in [301, 302, 503] and 'Location' in response.headers:
            yield scrapy.Request(response.headers['location'], callback=self.parse)
            return

        for item in response.xpath('//div[@id="resultsCol"]//li//div[@class="a-row a-spacing-small"]//a/@href').extract():
            item_url = response.urljoin(item)
            yield scrapy.Request(item_url, callback=self.parse_item)

        next_page = response.xpath('//a[@id="pagnNextLink"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        """
        Parse the page descring the item
        """
        def get_data(xpath):
            """
            Return the strip text of the given xpath
            """
            return response.xpath(xpath).extract_first().strip()

        price_text = get_data('//span[@id="priceblock_ourprice"]/text()').split(' ')

        yield {
            'product': get_data('//h1[@id="title"]/span/text()'),
            'brand': get_data('//div[@id="brandByline_feature_div"]//a[@id="brand"]/text()'),
            'currency': price_text[0],
            'price': float(price_text[1])
        }
