import re
import os
import json


def get_email_info(data):
    r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
    return r.findall(data)


def get_tel_info(data):
    r = re.compile('\(?\+?\d{0,2}\)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{3}')
    return r.findall(data)


def dump_contact_info(contact_info, file_ref):
    file_ref.write(json.dumps(contact_info) + "\n")


class ContactExtractionPipeline(object):

    # def open_spider(self, spider):
    #     self.file = open('contacts.jl', 'w')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        response_text = item["response_text"]
        contact_info = dict()

        contact_info["email"] = get_email_info(response_text)
        contact_info["tel"] = get_tel_info(response_text)
        contact_info["title"] = item["title"]

        filename = "contact/" + item["title"] + ".json"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "a") as f:
            dump_contact_info(contact_info, f)

        # line = json.dumps(email_info) + " " + json.dumps(contact_info) + "\n"
        # self.file.write(line)
        return item
