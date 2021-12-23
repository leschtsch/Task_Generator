"""
Данный модуль нужен, чтобы установить нужные модули, если их нет.
"""

import sys
import subprocess
import pkg_resources
from tkinter import *
from tkinter import messagebox


def setup():
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
        return True

    root = Tk()  # предупреждение о долгой установке
    root.withdraw()
    ok = messagebox.askyesno(title='установка',
                             message='''На компьютере нет некоторых модулей. Вы готовы начать установку?
Убедитесь в наличии подключения к Интернету для усановки. Установка может быть долгой.''')
    if not ok:
        return False

    '''
    установка модулей
    Я написал три варианта, потому что не знаю,
    что из этого на каком компьютере сработает.
    В коде со StackOverFlow был check_call, но он устарел
    '''
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', *missing], check=True)
        return True
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.run(['pip', 'install', *missing], check=True)
        return True
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.run(['pip3', 'install', *missing], check=True)
        return True
    except subprocess.CalledProcessError:
        pass

    messagebox.showerror('установка', 'ошибка установки')
    return False
    # установка модулей
