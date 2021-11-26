from docx import Document


class PageBreak:
    def __init__(self):
        pass

    def insert(self, doc: Document):
        doc.paragraphs[-1].add_run()
        doc.paragraphs[-1].runs[-1].add_break(7)
