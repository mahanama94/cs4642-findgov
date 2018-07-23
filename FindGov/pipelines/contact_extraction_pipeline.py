import re
import os


def get_email_info(data):
    r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
    return r.findall(data)


def get_contact_info(data):
    r = re.compile('\(?\+?\d{0,2}\)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{3}')
    return r.findall(data)


def dump_email_info(email_info, file_ref):
    for email_address in email_info:
        file_ref.write(email_address)


def dump_contact_info(contact_info, file_ref):
    for contact_number in contact_info:
        file_ref.write(contact_number)


class ContactExtractionPipeline(object):

    # def open_spider(self, spider):
    #     self.file = open('contacts.jl', 'w')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        response_text = item["response_text"]
        email_info = get_email_info(response_text)
        contact_info = get_contact_info(response_text)

        filename = "contact/" + item["title"] + ".txt"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "a") as f:
            dump_contact_info(contact_info, f)
            dump_email_info(email_info, f)

        # line = json.dumps(email_info) + " " + json.dumps(contact_info) + "\n"
        # self.file.write(line)
        return item
