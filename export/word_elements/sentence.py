from docx import Document


class Sentence:
    """
    Класс, позволяющий вставить другие элементы (кроме List) в один абзац.
    """
    def __init__(self, elements: list):
        """
        :param elements: список элементов для вставки.
        """
        self.elements = elements

    def insert(self, doc: Document):
        """
        Функция, вставляющая элементы в новый абзац документа.
        :param doc: python_docx Document, в который нужно вставить элементы.
        """
        for element in self.elements:
            element.insert(doc)
