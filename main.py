import sys
import os.path
import time
import subprocess
import pkg_resources


def install_modules():
    required = {'pygame', 'pygame-gui', 'python-docx', 'lxml', 'easygui', 'latex2mathml'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])


install_modules()

from easygui import fileopenbox, filesavebox

from export import export
from interface import Interface


def generator_load():
    generator = fileopenbox(msg='Выберите генератор', default='Генераторы/generator.py',
                            filetypes=['*.py'])
    if not generator:
        return None
    generator = list(os.path.split(generator))
    sys.path.append(generator[0])
    sys.path.append(os.path.join(generator[0], 'subgenerators'))
    generator[1] = generator[1].strip('.py')
    generator = __import__(generator[1])
    return generator.Generator()


generator = generator_load()
if generator:
    interface = Interface(generator.window_size, generator.needed_params, generator.status)

    for i in generator.needed_params:
        if i.name in generator.selected_params and (i.type_ == 'text' or i.type_ == 'number'):
            interface.widgets[i.name][1].set_text(generator.selected_params[i.name])

    running = True

    while running:
        time.sleep(0.01)
        interface.status = generator.status
        interface.ready = generator.ready

        params = interface.tick()
        if isinstance(params, dict):
            generator.set_params(params)
        elif params == 'Generate':
            interface.status = 'генерация задач'
            interface.tick()
            tasks, answers = generator.generate()
            interface.status = 'сохранение задач'
            interface.tick()
            save_path = filesavebox(msg='сохранение файла', default='задания')
            if save_path:
                export(tasks, answers, save_path)
                interface.generated += 1
            interface.status = generator.status
            interface.tick()
        else:
            break
