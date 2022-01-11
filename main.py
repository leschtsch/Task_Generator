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
            pass
        else:
            break


if installed:
    mainloop()
