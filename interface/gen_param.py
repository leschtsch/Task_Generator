"""
В данном модуле хранится класс GeneratorParameter,
который используется генераторами для описания нужных ему виджетов и параметров.
"""

from pygame import Rect
from typing import Tuple


class GeneratorParameter:
    """
    Этот класс используется, чтобы описывать нужные генератору параметры и виджеты.
    Он просто хранит имя параметра, тип виджета, положение виджета, описание и некоторые специфичные опции.
    """

    def __init__(self, name: str, type_: str, relative_rect: Tuple[int, int, int, int], description: str = '',
                 **kwargs):
        """

        :param name: имя, под которым параметр будет передаваться в генератор
        :param type_: Тип виджета, который нужен генератору. Существуют следующие:
            text - поле ввода текста.
            number - поле ввода числа. То же, что и предыдущее, но не дает ввести не число.
            radio_list - список выбора одного элемента.
            check_list - список выбора нескольких элементов.
            slider - горизонтальный ползунок.
        :param relative_rect: координаты левого верхнего угла, длина и ширина виджета.
        :param description: Описание виджета, которое отобразится в интерфейсе.
        :param kwargs: Специфические параметры. Пока что есть 'options' и 'value_range'. Подробнее ниже.
        """
        self.name = name
        self.type_ = type_
        self.relative_rect = Rect(relative_rect[0], relative_rect[1], relative_rect[2], relative_rect[3])
        if 'options' in kwargs:  # options - список опций для выбора списка. Только для check_list и radio_list.
            self.options = kwargs['options']
        if 'value_range' in kwargs:  # value_range - кортеж крайних значений для слайдера.
            self.value_range = kwargs['value_range']
        self.description = description

    def __repr__(self):
        return self.name
