from docx import Document


class Text:
    def __init__(self, text=''):
        self.text = text

    def insert(self, doc: Document):
        doc.paragraphs[-1].add_run(self.text)
