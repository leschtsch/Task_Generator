from os import getcwd

from interface import GeneratorParameter as P
from export.word_elements import *
from export.word import to_docx


class Generator:
    def __init__(self):
        self.window_size = (500, 500)

        self.needed_params = []
        self.selected_params = {}

        self.status = 'Это тестовый генератор.'
        self.generated = 0
        self.ready = True
        self.new_params = False

    def set_params(self, params):
        pass

    def generate(self):
        els = [
            List([Text('тест'),
                  LatexFormula('x^2=0', space=1),
                  Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=5)], style='number'),
            Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=10),
            PageBreak(),
            Sentence([Text('тест '),
                      Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=1, inline=True),
                      Text(' '), LatexFormula('x^2=0', space=1)])
        ]
        to_docx(els, 'тест')
