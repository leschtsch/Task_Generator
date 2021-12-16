from docx import Document
from docx.shared import Cm


class Picture:
    def __init__(self, path, width=None, height=None, inline=False):
        self.path = path
        self.width = None if width is None else Cm(width)
        self.height = None if height is None else Cm(height)
        self.inline = inline

    def insert(self, doc: Document):
        if self.inline:
            doc.paragraphs[-1].runs[-1].add_picture(self.path, width=self.width, height=self.height)
        else:
            doc.add_picture(self.path, width=self.width, height=self.height)
