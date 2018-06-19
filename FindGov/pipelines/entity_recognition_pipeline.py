
from nltk import ne_chunk


class EntityRecognitionPipeline(object):
    def open_spider(self, spider):
        self.file = open('entities.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        tagged = item["pos_tags"]
        chunks = ne_chunk(tagged, binary=True)
        item["entities"] = self.get_named_entities(chunks)
        self.file.write(' '.join([item for pos, item in item["entities"]]))
        return item

    # def get_continuous_chunks(self, chunked):
    #     prev = None
    #
    #     continuous_chunk = []
    #
    #     current_chunk = []
    #
    #     for i in chunked:
    #
    #         if type(i) == Tree:
    #             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    #         elif current_chunk:
    #             named_entity = " ".join(current_chunk)
    #             if named_entity not in continuous_chunk:
    #                 continuous_chunk.append(named_entity)
    #                 current_chunk = []
    #         else:
    #             continue
    #     return continuous_chunk

    def get_named_entities(self, chunks):
        entity_list = list()
        for chunk in chunks:
            if hasattr(chunk, 'label'):
                entity_list.append((chunk.label(), ' '.join(c[0] for c in chunk)))
        return entity_list