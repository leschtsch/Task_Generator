from docx import Document


class Sentence:
    def __init__(self, elements):
        self.elements = elements

    def insert(self, doc: Document):
        for element in self.elements:
            element.insert(doc)
