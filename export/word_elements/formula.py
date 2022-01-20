import pathlib
import os

from docx import Document
from lxml import etree  # чтобы конвертировать MML в OMML
import latex2mathml.converter  # чтобы конвертировать LaTeX в MMl


class LatexFormula:
    """
    Данный класс используется для вставки в docx формулы. Некоторые функции теряются при конвертации,
    но в остальном работает.
    """
    def __init__(self, latex: str, space: float = 3.0):
        """
        :param latex: строка с формулой LaTex, без дополнительных символов.
        :param space: отступ строки вокруг формулы.
        """
        self.space = space
        self.latex = latex
        mathml = latex2mathml.converter.convert(self.latex)
        tree = etree.fromstring(mathml)
        xslt = etree.parse(str(next(pathlib.Path(os.getcwd()).glob('**/MML2OMML.xsl'))))
        transform = etree.XSLT(xslt)
        new_dom = transform(tree)
        self.xml = new_dom.getroot()

    def insert(self, doc: Document):
        """
        Функция, вставляющая формулу в документ.
        :param doc: python_docx Document, в который нужно вставить формулу.
        """
        doc.paragraphs[-1].add_run(' ')
        doc.paragraphs[-1]._element.append(self.xml)
        doc.paragraphs[-1].paragraph_format.line_spacing = self.space
