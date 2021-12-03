import time

from interface import GeneratorParameter as P
from export.word_elements import *
from export.word import to_docx


class Generator:
    def __init__(self):
        self.window_size = (730, 500)

        self.__always_needed_params = [
            P(name='task_types', type_='check_list', relative_rect=(20, 100, 350, 126), description='тип задачи:',
              options=[
                  '1. Перевод обыкновенные - смешанные',
                  '2. +/- с одинаковыми знаменателями',
                  '3. +/- с взаимно простыми знаменателями',
                  '4. +/- с кратными знаменателями',
                  '5. +/- со знаменателями с общим множителем',
                  '6. +/- с любыми знаменателями'
              ])
        ]

        self.__selected_themes = []

        self.needed_params = self.__always_needed_params.copy()

        self.selected_params = {
        }

        self.status = 'ожидание параметров'
        self.generated = 0
        self.ready = False
        self.new_params = False

    def set_params(self, params):
        themes = {
            '1. Перевод обыкновенные - смешанные': '1',
            '2. +/- с одинаковыми знаменателями': '2',
            '3. +/- с взаимно простыми знаменателями': '3',
            '4. +/- с кратными знаменателями': '4',
            '5. +/- со знаменателями с общим множителем': '5',
            '6. +/- с любыми знаменателями': '6'
        }

        for i in params:
            self.selected_params[i] = params[i]

        self.ready = True
        self.status = 'генератор готов к работе'

        if set(self.selected_params['task_types']) != set(self.__selected_themes):
            self.status = 'ожидание параметров'
            self.new_params = True
            self.ready = False
            c = 0
            self.needed_params = self.__always_needed_params.copy()
            for i in self.selected_params['task_types']:
                theme = themes[i]
                self.needed_params.append(
                    P(name=theme + 'difficulty_level', type_='slider', relative_rect=(410, 100 + c * 50, 110, 20),
                      description='уровень сложности %s:' % theme,
                      value_range=[1, 3]))
                self.needed_params.append(
                    P(name=theme + 'quantity', type_='number', relative_rect=(540, 100 + c * 50, 100, 20),
                      description='количество заданий %s:' % theme))
                c += 1
            self.__selected_themes = self.selected_params['task_types'].copy()

        if not self.__selected_themes:
            self.ready = False
            self.status = 'ожидание параметров'

    def __get_save_name(self):
        themes = {
            '1. Перевод обыкновенные - смешанные': 'перевод',
            '2. +/- с одинаковыми знаменателями': 'одинак.знам',
            '3. +/- с взаимно простыми знаменателями': 'вз.пр.знам.',
            '4. +/- с кратными знаменателями': 'кратн.знам',
            '5. +/- со знаменателями с общим множителем': 'общ.мн.',
            '6. +/- с любыми знаменателями': 'НОД и НОК'
        }
        return 'Алгебра-об.дроби-%s' % time.strftime('%d.%m_%H.%M.%S', time.gmtime(time.time()))
        # TODO: local time

    def generate(self):
        descs = [
            'Переведите обыкновенные дроби в смешанные, а смешанные - в обыкновенные.',
            'Решите примеры.'
        ]
        tels, aels = [], []
        tasknum = 1
        if '1. Перевод обыкновенные - смешанные' in self.selected_params['task_types']:
            import subgenerator1
            task = str(tasknum) + '. ' + descs[0]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator1.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])
        if '2. +/- с одинаковыми знаменателями' in self.selected_params['task_types']:
            import subgenerator2
            task = str(tasknum) + '. ' + descs[1]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator2.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])
        if '3. +/- с взаимно простыми знаменателями' in self.selected_params['task_types']:
            import subgenerator3
            task = str(tasknum) + '. ' + descs[1]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator3.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])
        if '4. +/- с кратными знаменателями' in self.selected_params['task_types']:
            import subgenerator4
            task = str(tasknum) + '. ' + descs[1]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator4.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])
        if '5. +/- со знаменателями с общим множителем' in self.selected_params['task_types']:
            import subgenerator5
            task = str(tasknum) + '. ' + descs[1]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator5.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])
        if '6. +/- с любыми знаменателями' in self.selected_params['task_types']:
            import subgenerator6
            task = str(tasknum) + '. ' + descs[1]
            ans = str(tasknum) + '. ' + 'Ответы.'
            tasknum += 1
            tasks, answers = subgenerator6.generate(self.selected_params)
            tels.extend([Text(task), List([LatexFormula(i) for i in tasks], style='number')])
            aels.extend([Text(ans), List([LatexFormula(i) for i in answers], style='number')])

        name = self.__get_save_name()
        els = [*tels, PageBreak(), *aels]
        path = to_docx(els, name)
        if path is not None:
            self.generated += 1
