from os import getcwd

from interface import GeneratorParameter as P
from export.word_elements import *
from export.word import to_docx

import pygame
from export.altTeX import alttex


class Generator:
    def __init__(self):
        self.name = 'Тест'

        self.window_size = (700, 500)

        self.needed_params = []
        self.selected_params = {}

        self.status = 'Это тестовый генератор.'
        self.generated = 0
        self.ready = True
        self.new_params = False

    def set_params(self, params):
        pass

    def generate(self):
        tels = [
            List([Text('тест'),
                  LatexFormula('x^2=0', space=1),
                  Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=5)], style='number'),
            Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=10),
        AlttexFormula('A3A(c(t(   y = ))(sqrt(t(x))))(c(t(   y = x))(i(t(2))()))(c(t(   y = ))(|(t(x))(t(x+1))))')]
        aels = [
            Sentence([Text('тест '),
                      Picture(getcwd() + '\\Генераторы\\Тест\\subgenerators\\coh.png', width=1, inline=True),
                      Text(' '), LatexFormula('x^2=0', space=1)])]
        return tels, aels
