import json
import random
from os import getcwd

from interface import GeneratorParameter as P
from export.word_elements import *
from export.word import to_docx


class Generator:
    def __init__(self):
        self.name = 'Физика Блоки'

        self.window_size = (650, 500)

        self.needed_params = [
            P(name='quantity', type_='number', relative_rect=(275, 240, 100, 20), description='количество задач:')
        ]
        self.selected_params = {'quantity': '10'}

        self.status = 'ожидание параметров'
        self.generated = 0
        self.ready = False
        self.new_params = False

    def set_params(self, params):
        self.ready = True
        self.status = 'Генератор готов к работе'

        for i in params:
            self.selected_params[i] = params[i]

        if not self.selected_params['quantity'].isdigit() or int(self.selected_params['quantity']) <= 0:
            self.ready = False
            self.status = 'Кол-во задач должно быть натуральным'

    def generate(self):
        problems = [
            'Груз массы M = %d г подвешен к подвижному блоку (см. рисунок).'
            ' Что показывает динамометр? Нити и блоки невесомы, трения нет.',

            'Система, состоящая из подвижного и неподвижного блоков и двух грузов,'
            ' показанная на рисунке, находится в равновесии. Масса левого груза m1 = %d кг,'
            ' масса каждого     из блоков равна m = %d кг, массой нитей можно пренебречь.'
            ' Найдите массу m2 правого груза. Трения нет.',

            'Два автомобиля едут в противоположные стороны со скоростями v =  и v2.'
            ' К одному автомобилю привязан трос, который переброшен через блок,'
            ' привязанный ко второму автомобилю.'
            ' Второй конец троса привязан к тележке (см. рисунок).'
            'Найти её скорость, если v = %d м/с, а v2 = %d м/с.'
        ]
        tasks = []
        answers = []
        for i in range(int(self.selected_params['quantity'])):
            random.seed(random.randint(1, 1000000))
            n = random.randint(1, 3)
            if n == 1:
                m = random.choice([i * 200 for i in range(1, 31)])
                tasks.append(Sentence([
                    Text(problems[0] % m + '\n'),
                    Picture(getcwd() + '\\Генераторы\\Физика\\Блоки\\subgenerators\\1.png', height=4, inline=True)
                ]))
                answers.append(Text(str(m // 200) + ' Н'))
            elif n == 2:
                m1 = random.randint(1, 10)
                m = random.randint(1, 10)
                tasks.append(Sentence([
                    Text(problems[1] % (m1, m) + '\n'),
                    Picture(getcwd() + '\\Генераторы\\Физика\\Блоки\\subgenerators\\2.png', height=4, inline=True)
                ]))
                answers.append(Text(str((m1 + m) / 2) + ' кг'))
            elif n == 3:
                v = random.randint(1, 10)
                v2 = random.randint(1, 10)
                tasks.append(Sentence([
                    Text(problems[2] % (v, v2) + '\n'),
                    Picture(getcwd() + '\\Генераторы\\Физика\\Блоки\\subgenerators\\3.png', width=5, inline=True)
                ]))
                answers.append(Text(str(v2 + 2 * v) + ' м/с'))

        return [List(tasks, style='number')], [List(answers, style='number')]
        # if to_docx([List(tasks, style='number'), PageBreak(), List(answers, style='number')],
        #            default='Блоки') is not None:
        #     self.generated += 1
