import typing

from docx import Document
from easygui import filesavebox

from export.word_elements import *


def to_docx(elements, default='Работа'):
    path = filesavebox(msg='сохранение файла', default=default)
    if not path:
        return

    d = Document()
    for i in elements:
        d.add_paragraph()
        i.insert(d)
    d.save(path + '.docx')
    return path


if __name__ == '__main__':
    el = [
        Text('fgfgjdgjdf '),
        LatexFormula(r'\int_0^\infty{e^x}'),
        List([
            Text('asd'),
            Text('as\ndf'),
            Text('asdf')
        ]),
        PageBreak(),
        List([
            LatexFormula(r'x^\omega'),
            LatexFormula(r'\frac{a}{\frac{a}{\frac{a}{b}}}'),
            LatexFormula(r'\int_0^\infty{e^x}')
        ], style='number'),
    ]

    to_docx(el)
