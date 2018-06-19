from bs4 import BeautifulSoup
import json

class TitleHandlerPipeline(object):
    def open_spider(self, spider):
        self.file = open('titles.jl', 'w')

    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):
        response_text = item['response'].text
        soup = BeautifulSoup(response_text, 'html.parser')
        title = soup.title.string
        line = json.dumps(title) + "\n"
        self.file.write(line)
        return item