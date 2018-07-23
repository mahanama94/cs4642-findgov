import os
import json
from nltk import ne_chunk


class EntityRecognitionPipeline(object):
    # def open_spider(self, spider):
    #     self.file = open('entities.jl', 'w')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        tagged = item["pos_tags"]
        chunks = ne_chunk(tagged, binary=True)
        entities = self.get_named_entities(chunks)
        entity_list = list()
        for entity in entities:
            entity_list.append(entity[1])

        entity_info = dict()
        entity_info["entities"] = entity_list
        entity_info["reference"] = item["response"].url

        filename = "entities/" + item["title"] + ".json"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "a") as f:
            f.write(json.dumps(entity_info) + "\n")

        item["entities"] = entity_info
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