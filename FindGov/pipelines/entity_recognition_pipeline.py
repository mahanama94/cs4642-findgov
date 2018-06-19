import re
import sys

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.tree import Tree


class EntityRecognitionPipeline(object):
    def open_spider(self, spider):
        self.file = open('entities.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response_text = item["response"].text
        non_tagged_response = re.sub("<.*?>", " ", response_text)
        word_tokens = word_tokenize(non_tagged_response)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in word_tokens if not w in stop_words]
        tagged = pos_tag(filtered_tokens)
        named_ent = ne_chunk(tagged, binary=True)
        chunks = self.get_continuous_chunks(named_ent)
        self.file.write(' '.join(chunks))
        return item

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
