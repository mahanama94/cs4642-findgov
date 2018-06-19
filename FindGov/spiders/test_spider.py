from bs4 import BeautifulSoup

import scrapy


class TestSpider(scrapy.Spider):
    name = "test"

    allowed_domains = ['gov.lk']

    def start_requests(self):
        urls = [
            'https://www.cbsl.gov.lk/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        response_text = response.text
        soup = BeautifulSoup(response_text, 'html.parser')
        anchors = soup.find_all('a')

        yield {
            "response" : response,
        }
