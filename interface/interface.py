import pygame_gui
import pygame
from easygui import fileopenbox

import typing
import re
import os
import sys
from importlib import invalidate_caches

from interface.gen_param import GeneratorParameter as P
from interface.widget_creator import create_widget


class Interface:
    def __init__(self, description=''):
        pygame.init()
        self.__window_size = (1100, 600)
        self.__screen = pygame.display.set_mode(self.__window_size)
        self.__screen.fill('#f0f0f0')
        self.__manager = pygame_gui.ui_manager.UIManager(self.__window_size)

        pygame.font.init()
        self.__font = pygame.font.SysFont('Arial', 15)
        self.__description_font = pygame.font.SysFont('Arial', 25, italic=True)
        self.__note_font = pygame.font.SysFont('Arial', 13, italic=True)

        self.__status = description
        self.__ready = False
        self.__generated = 0

        self.__widgets = {}

        self.__generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 540, 300, 50),
            manager=self.__manager,
            text='СГЕНЕРИРОВАТЬ'
        )
        self.__generate_button.is_enabled = self.__ready

        self.__generators_selection_list = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect(810, 30, 280, 200),
            manager=self.__manager,
            item_list=[]
        )
        self.__add_gen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(810, 240, 280, 50),
            manager=self.__manager,
            text='Добавить генератор'
        )
        self.__delete_gen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(810, 295, 280, 50),
            manager=self.__manager,
            text='Удалить выбранный генератор'
        )

        self.__generators = {}
        self.__current_generator = None

    def __generator_load(self):
        """
        Данная функция получает путь к файлу с генератором,
        используя easygui, после чего импортирует его и возвращает экземпляр класса генератора.
        :return: объект генератора.
        """
        generator_path = fileopenbox(msg='Выберите генератор', default='Генераторы/generator.py',
                                     filetypes=['*.py'])  # получение поти к генератору
        if not generator_path:
            return

        generator_path = list(os.path.split(generator_path))  # получение пути и имени модуля из пути к файлу
        generator_path[1] = generator_path[1].strip('.py')

        gen_name = generator_path[0].split('Генераторы')[1]
        gen_name = re.sub(r'\\', ' ', gen_name)

        if gen_name not in self.__generators:
            sys.path.append(generator_path[0])  # вставка пути чтобы сработал импорт
            sys.path.append(os.path.join(generator_path[0], 'subgenerators'))

            generator = __import__(generator_path[1])  # импорт
            generator = generator.Generator()
            self.__generators[gen_name] = generator
            self.__generators_selection_list.set_item_list(
                [i['text'] for i in self.__generators_selection_list.item_list] + [gen_name]
            )

            sys.path.remove(generator_path[0])  # удаление пути чтобы не засорять этот список
            sys.path.remove(os.path.join(generator_path[0], 'subgenerators'))

    def __generator_delete(self):
        name = self.__generators_selection_list.get_single_selection()
        if name is None:
            return

        il = self.__generators_selection_list.item_list
        il = [i['text'] for i in il]
        il.remove(name)
        self.__generators_selection_list.set_item_list(il)

        del self.__generators[name]
        self.__current_generator = None
        self.__set_params()

    def __check_integers(self):
        for i in self.__widgets:
            if not self.__widgets[i][1].is_focused and self.__widgets[i][0].type_ == 'number':
                numbers = re.findall(r'-?\d*\.\d+|-?\d+', self.__widgets[i][1].get_text())
                if numbers:
                    self.__widgets[i][1].set_text(numbers[0])
                else:
                    self.__widgets[i][1].set_text('0')

    def __check_sliders(self):
        for i in self.__widgets:
            if self.__widgets[i][0].type_ == 'slider':
                a = self.__widgets[i][1]
                if not a.is_focused and not a.left_button.is_focused and not a.right_button.is_focused:
                    '''Если не сделать следующую строчку, то ползунок можно будет поставить, где угодно.
                    А хочется, чтобы для ползунка было несколько фиксированных позиций.'''
                    a.set_current_value(a.get_current_value())

    def __draw(self):
        self.__screen.fill('#f0f0f0')

        label = self.__description_font.render(self.__status, True, (0, 0, 0))
        self.__screen.blit(label, label.get_rect(midtop=(400, 30)))

        label = self.__note_font.render('задания сохранены %d раз(а)' % self.__generated, True, (0, 0, 0))
        self.__screen.blit(label, label.get_rect(topleft=(570, 550)))

        for i in self.__widgets:
            label = self.__font.render(self.__widgets[i][0].description, True, (0, 0, 0))
            self.__screen.blit(label, label.get_rect(bottomleft=self.__widgets[i][0].relative_rect.topleft))

            if self.__widgets[i][1].is_focused:
                label = self.__note_font.render('изменения не сохранены', True, (0, 0, 0))
                self.__screen.blit(label, label.get_rect(topleft=self.__widgets[i][0].relative_rect.topright))

            if self.__widgets[i][0].type_ == 'slider':
                label = self.__note_font.render(str(self.__widgets[i][1].get_current_value()), True, (0, 0, 0))
                self.__screen.blit(label, label.get_rect(topleft=self.__widgets[i][0].relative_rect.bottomleft))

        # Вкладка с генераторами
        pygame.draw.rect(self.__screen, '#aaaaaa', (800, -5, 1105, 605))
        pygame.draw.line(self.__screen, '#777777', (800, 0), (800, 600))

        label = self.__font.render('Генераторы:', True, (0, 0, 0))
        self.__screen.blit(label, label.get_rect(topleft=(810, 10)))
        # Вкладка с генераторами

    def __get_params(self):
        answer = {}
        for i in self.__widgets:
            if not self.__widgets[i][1].is_focused:
                type_ = self.__widgets[i][0].type_
                if type_ == 'text' or type_ == 'number':
                    answer[i] = self.__widgets[i][1].get_text()
                elif type_ == 'radio_list':
                    answer[i] = self.__widgets[i][1].get_single_selection()
                elif type_ == 'check_list':
                    answer[i] = self.__widgets[i][1].get_multi_selection()
                elif type_ == 'slider':
                    answer[i] = self.__widgets[i][1].get_current_value()
        return answer

    def __set_params(self, widget_list: typing.List[P] = None, default=None):
        params = self.__get_params()

        for i in self.__widgets:
            self.__widgets[i][1].kill()

        self.__widgets = {}
        if widget_list is not None:
            for i in widget_list:
                self.__widgets[i.name] = (i, create_widget(i, self.__manager))
        self.__ready = False

        for i in params:
            if i in self.__widgets:
                if self.__widgets[i][0].type_ in ['number', 'text']:
                    self.__widgets[i][1].set_text(params[i])
                elif self.__widgets[i][0].type_ == 'radio_list':
                    sl = self.__widgets[i][1]
                    il = [i['text'] for i in sl.item_list]
                    event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                  'ui_element': sl.item_list_container.elements[sl.item_list.index(params[i])]}
                    press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                    self.__manager.process_events(press_list_item_event)
                elif self.__widgets[i][0].type_ == 'check_list':
                    sl = self.__widgets[i][1]
                    il = [i['text'] for i in sl.item_list]
                    for j in params[i]:
                        event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                      'ui_element': sl.item_list_container.elements[il.index(j)]}
                        press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                        self.__manager.process_events(press_list_item_event)
                elif self.__widgets[i][0].type_ == 'slider':
                    self.__widgets[i][1].set_current_value(params[i])

        if default is not None:
            for i in default:
                if i in self.__widgets and i not in params:
                    if self.__widgets[i][0].type_ in ['number', 'text']:
                        self.__widgets[i][1].set_text(default[i])
                    elif self.__widgets[i][0].type_ == 'radio_list':
                        sl = self.__widgets[i][1]
                        il = [i['text'] for i in sl.item_list]
                        event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                      'ui_element': sl.item_list_container.elements[sl.item_list.index(default[i])]}
                        press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                        self.__manager.process_events(press_list_item_event)
                    elif self.__widgets[i][0].type_ == 'check_list':
                        sl = self.__widgets[i][1]
                        il = [i['text'] for i in sl.item_list]
                        for j in default[i]:
                            event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                          'ui_element': sl.item_list_container.elements[il.index(j)]}
                            press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                            self.__manager.process_events(press_list_item_event)
                    elif self.__widgets[i][0].type_ == 'slider':
                        self.__widgets[i][1].set_current_value(default[i])

    def tick(self):
        if self.__current_generator is not None and self.__current_generator.new_params:
            self.__set_params(self.__current_generator.needed_params, self.__current_generator.selected_params)
            self.__current_generator.new_params = False
        if self.__current_generator is not None:
            self.__status = self.__current_generator.status
        else:
            self.__status = 'откройте генераторы'
        self.__generate_button.is_enabled = self.__ready
        self.__delete_gen_button.is_enabled = self.__current_generator is not None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__generate_button:
                        return 'Generate'
                    elif event.ui_element == self.__add_gen_button:
                        self.__generator_load()
                    elif event.ui_element == self.__delete_gen_button:
                        self.__generator_delete()
                elif event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_element == self.__generators_selection_list:
                        self.__current_generator = self.__generators[event.text]
                        self.__set_params(self.__current_generator.needed_params,
                                          self.__current_generator.selected_params)
            self.__manager.process_events(event)

        for i in self.__widgets:
            if self.__widgets[i][0].type_ == 'check_list' or self.__widgets[i][0].type_ == 'radio_list':
                self.__widgets[i][1].unfocus()

        self.__check_integers()
        self.__check_sliders()
        self.__manager.update(0.01)
        self.__draw()
        self.__manager.draw_ui(self.__screen)
        pygame.display.update()

        params = self.__get_params()
        if self.__current_generator is not None:
            self.__current_generator.set_params(params)
        return params
