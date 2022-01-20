from interface import GeneratorParameter as GenP  # параметры генератора
from export.word_elements import *  # элементы экспорта
import random


class Generator:
    def __init__(self):
        self.status = 'Здесь пока ничего нет'
        self.generated = 0
        self.ready = False
        self.new_params = False

        self.__flag = True

        self.needed_params = [
            GenP(name='quantity', type_='number', relative_rect=(300, 100, 100, 30), description='Количество задач')
        ]

        self.selected_params = {}

    def set_params(self, params):
        self.new_params = False # чтобы параметры не переустанавливались снова
        self.ready = True  # разблокирует кнопку генерации
        self.status = 'Генератор готов'  # отобразится в интерфейсе
        for i in params:
            self.selected_params[i] = params[i]
        if not self.selected_params['quantity'].isdigit() or int(self.selected_params['quantity']) <= 0:
            self.ready = False  # заблокирует кнопку генерации
            self.status = 'Количество задач должно быть натуральным числом'  # отобразится в интерфейсе
        if self.__flag and int(self.selected_params['quantity']) > 3:  # флаг отвечает за отсутствие виджета
            self.new_params = True
            self.ready = False
            self.__flag = False
            self.status = 'Ожидание параметров'
            self.needed_params.append(
                GenP(name='txt', type_='text', relative_rect=(300, 200, 100, 30), description='текст'))
            self.selected_params['txt'] = 'текст'  # вариант по умолчанию

    def generate(self):
        tasks, answers = [], []
        for i in range(int(self.selected_params['quantity'])):
            a, b = random.randint(1, 100), random.randint(1, 100)
            c = a + b
            tasks.append(LatexFormula('%d + %d' % (a, b)))
            answers.append(LatexFormula('%d + %d = %d' % (a, b, c)))
        return [
                   Text('Решите примеры:'),
                   List(elements=tasks, style='number')
               ], [
                   List(elements=answers, style='number')
               ]
