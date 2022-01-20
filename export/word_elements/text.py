from docx import Document


class Text:
    """
    Класс, описывающий текст в документе.
    """

    def __init__(self, text: str = ''):
        """
        :param text: текст для вставки.
        """
        self.text = text

    def insert(self, doc: Document):
        """
        Функция, вставляющая текст в документ.
        :param doc: python_docx Document, в который нужно вставить текст.
        """
        doc.paragraphs[-1].add_run(self.text)
