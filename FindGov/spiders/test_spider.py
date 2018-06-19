import scrapy
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.tree import Tree
import sys

class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        urls = [
            'https://www.cbsl.gov.lk/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response_text = response.text
        soup = BeautifulSoup(response_text, 'html.parser')
        title = soup.title.string
        anchors = soup.find_all('a')


        non_tagged_response = re.sub("<.*?>", " ", response_text)
        word_tokens = word_tokenize(non_tagged_response)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in word_tokens if not w in stop_words]
        tagged = nltk.pos_tag(filtered_tokens)
        namedEnt = nltk.ne_chunk(tagged, binary=True)
        chunks = self.get_continuous_chunks(namedEnt)

        filename = 'scrape.html'
        with open(filename, 'wb') as f:
            f.write("\n".join(chunks))

        self.log('Saved file %s' % filename)

    def get_continuous_chunks(self, chunked):
        prev = None

        continuous_chunk = []

        current_chunk = []

        for i in chunked:

            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue
        return continuous_chunk