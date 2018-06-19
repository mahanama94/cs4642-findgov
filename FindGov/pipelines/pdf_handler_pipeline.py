import urllib2
import io
import PyPDF2

class PDFHandlerPipeline(object):
    def open_spider(self, spider):
        self.file = open('pdf.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        response = item['response']
        if 'pdf' in response.headers.get('Content-Type'):
            data = urllib2.urlopen(response.url)
            memory_file = io.BytesIO(data.read())

            read_pdf = PyPDF2.PdfFileReader(memory_file)
            number_of_pages = read_pdf.getNumPages()

            page_data = []
            for i in range(0, number_of_pages):
                pageObj = read_pdf.getPage(i)
                page = pageObj.extractText()
                page_data.append(page)

            item["response_text"] = " ".join(page_data)
            print(item["response_text"])
            self.file.write(" ".join(page_data))
        return item