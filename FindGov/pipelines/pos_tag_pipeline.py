import re
import sys

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

class PosTagPipeline(object):
    def open_spider(self, spider):
        self.file = open('entities.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response_text = item["response_text"]
        non_tagged_response = re.sub("<.*?>", " ", response_text)
        word_tokens = word_tokenize(non_tagged_response)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in word_tokens if not w in stop_words]
        tagged = pos_tag(filtered_tokens)
        item["pos_tags"] = tagged
        return item