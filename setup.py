"""
Данный модуль нужен, чтобы установить нужные модули, если их нет.
"""

import sys
import subprocess
import pkg_resources
from tkinter import *
from tkinter import messagebox


def install_missing():
    """
    Данная функция устанавливает необходимые модули
    :return: None
    """

    # получение множества недостающих модулей
    required = {'pygame', 'pygame-gui', 'python-docx', 'lxml', 'easygui', 'latex2mathml'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    # получение множества недостающих модулей

    if not missing:  # проверка, надо ли что-то устанавливать
        return

    root = Tk()  # предупреждение о болгой установке
    root.withdraw()
    messagebox.showinfo('', 'Запуск может быть долгим.\nНажмите ОК')

    '''
    установка модулей
    Я написал три варианта, потому что не знаю,
    что из этого на каком компьютере сработает.
    В коде со StackOverFlow был check_call, но он устарел
    '''
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', *missing], check=True)
        return
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.run(['pip', 'install', *missing], check=True)
        return
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.run(['pip3', 'install', *missing], check=True)
        return
    except subprocess.CalledProcessError:
        pass
    # установка модулей


install_missing()
