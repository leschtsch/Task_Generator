"""
Данный модуль реализует основной цикл программы.
"""

import sys
import os.path
import time

from setup import setup

installed = setup()
if installed:
    from easygui import fileopenbox, filesavebox  # чтобы открыть генератор и сохранить задачи

from interface import *
from export.word import *


def mainloop():
    """
    Данная функция реализует основной цикл программы.
    :param generator: объект - генератор
    :return: None
    """
    # создание интерфейса и задание параметров по умолчанию
    interface = Interface('откройте генераторы')

    running = True
    while running:
        time.sleep(0.01)  # иначе курсор ввода текста мерцает
        params = interface.tick()  # получение параметров генератора от интерфейса
        if isinstance(params, dict):
            pass
        elif params == 'Generate':
            tasks, answers = [], []
            for i in interface.generators:
                tasks.append(Text(i))
                answers.append(Text(i))
                gen = interface.generators[i]
                task, answer = gen.generate()
                tasks.extend(task)
                answers.extend(answer)
            if to_docx([*tasks, PageBreak(), Text('Ответы'), *answers]):
                interface.generated += 1
        else:
            break


if installed:
    mainloop()
