"""
Данный модуль импортирует генератор и реализует основной цикл программы.
"""

import sys
import os.path
import time

import setup
from easygui import fileopenbox, filesavebox  # чтобы открыть генератор и сохранить задачи

from export import export
from interface import Interface


def generator_load():
    """
    Данная функция получает путь к файлу с генератором,
    используя easygui, после чего импортирует его и возвращает экземпляр класса генератора.
    :return: объект генератора.
    """
    generator = fileopenbox(msg='Выберите генератор', default='Генераторы/generator.py',
                            filetypes=['*.py'])  # получение поти к генератору
    if not generator:
        return

    generator = list(os.path.split(generator))  # получение пути и имени модуля из пути к файлу
    generator[1] = generator[1].strip('.py')

    sys.path.append(generator[0])  # вставка пути чтобы сработал импорт
    sys.path.append(os.path.join(generator[0], 'subgenerators'))

    generator = __import__(generator[1])  # импорт
    return generator.Generator()


def mainloop(generator):
    """
    Данная функция реализует основной цикл программы.
    :param generator: объект - генератор
    :return: None
    """
    if generator is None:
        return

    # создание интерфейса и задание параметров по умолчанию
    interface = Interface(generator.window_size, generator.needed_params, generator.status)
    for i in generator.needed_params:
        if i.name in generator.selected_params and (i.type_ == 'text' or i.type_ == 'number'):
            interface.widgets[i.name][1].set_text(generator.selected_params[i.name])
    # создание интерфейса и задание параметров по умолчанию

    running = True
    while running:
        time.sleep(0.01)  # иначе курсор ввода текста мерцает

        # установка в интерфейс статусов генератора
        interface.status = generator.status
        interface.ready = generator.ready
        # установка в интерфейс статусов генератора

        params = interface.tick()  # получение параметров генератора от интерфейса
        if isinstance(params, dict):
            generator.set_params(params)
        elif params == 'Generate':
            interface.status = 'генерация задач'
            interface.tick()
            generated = generator.generate()  # [tasks, answers, default name]
            tasks = generated[0]
            answers = generated[1]
            interface.status = 'сохранение задач'
            interface.tick()
            save_path = filesavebox(msg='сохранение файла', default=generated[2])
            if save_path is not None:
                export(tasks, answers, save_path)
                interface.generated += 1
            interface.status = generator.status
            interface.tick()
        else:
            break


mainloop(generator_load())
