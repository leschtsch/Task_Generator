from interface import GeneratorParameter as P
import os
import sys


class Generator:
    def __init__(self):
        self.window_size = (800, 600)

        self.needed_params = [
            P(name='task_type', type_='radio_list', relative_rect=(20, 100, 350, 126), description='тип задачи:',
              options=[
                  'Перевод обыкновенные - смешанные',
                  '+/- с одинаковыми знаменателями',
                  '+/- с взаимно простыми знаменателями',
                  '+/- с кратными знаменателями',
                  '+/- со знаменателями с общим множителем',
                  '+/- с любыми знаменателями'
              ]),
            P(name='difficulty_level', type_='radio_list', relative_rect=(20, 251, 300, 66),
              description='уровень сложности:',
              options=['1', '2', '3']),
            P(name='quantity', type_='number', relative_rect=(20, 342, 100, 20), description='количество заданий:'),
        ]

        self.selected_params = {
            'quantity': '10'
        }

        self.status = 'ожидание параметров'
        self.ready = False

    def set_params(self, params):
        for i in params:
            self.selected_params[i] = params[i]

        self.ready = True
        self.status = 'генератор готов к работе'
        if not self.selected_params['task_type']:
            self.ready = False
            self.status = 'ожидание параметров'
        if not self.selected_params['difficulty_level']:
            self.ready = False
            self.status = 'ожидание параметров'
        if not self.selected_params['quantity'].isdigit() or int(self.selected_params['quantity']) < 1:
            self.ready = False
            self.status = 'количество задач должно быть целым и больше 0'

    def generate(self):
        if self.selected_params['task_type'] == 'Перевод обыкновенные - смешанные':
            import subgenerator1
            return subgenerator1.generate(self.selected_params)
        elif self.selected_params['task_type'] == '+/- с одинаковыми знаменателями':
            import subgenerator2
            return subgenerator2.generate(self.selected_params)
        elif self.selected_params['task_type'] == '+/- с взаимно простыми знаменателями':
            import subgenerator3
            return subgenerator3.generate(self.selected_params)
        elif self.selected_params['task_type'] == '+/- с кратными знаменателями':
            import subgenerator4
            return subgenerator4.generate(self.selected_params)
        elif self.selected_params['task_type'] == '+/- со знаменателями с общим множителем':
            import subgenerator5
            return subgenerator5.generate(self.selected_params)
        elif self.selected_params['task_type'] == '+/- с любыми знаменателями':
            import subgenerator6
            return subgenerator6.generate(self.selected_params)
