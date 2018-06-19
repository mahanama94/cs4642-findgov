from bs4 import BeautifulSoup

import scrapy


class MainSpider(scrapy.Spider):
    name = "test"

    allowed_domains = ['gov.lk']

    count = 5

    def start_requests(self):
        urls = [
            # 'https://www.cbsl.gov.lk/',
            'https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/press/pr/press_20180404_Monetary_Policy_Review_No_2_2018_e_U45p3.pdf'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            response_text = response.text
            soup = BeautifulSoup(response_text, 'html.parser')
            links = soup.find_all('a', href=True)

            # for link in links:
            #     if self.count < 10:
            #         if "#" not in link:
            #             yield scrapy.Request(response.urljoin(link["href"]), callback=self.parse)
            #
            # self.count += 1
            yield {
                "response": response,
                "response_text": response.text
            }

        except:
            self.log("Response Text Not Available")
            yield {
                "response": response,
            }
