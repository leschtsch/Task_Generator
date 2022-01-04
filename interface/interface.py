import pygame_gui
import pygame
from interface.gen_param import GeneratorParameter as P
from interface.widget_creator import create_widget
import typing
import re


class Interface:
    def __init__(self, widget_list: typing.List[P], description=''):
        pygame.init()
        self.__window_size = (800, 600)
        self.__screen = pygame.display.set_mode(self.__window_size)
        self.__screen.fill('#f0f0f0')
        self.__manager = pygame_gui.ui_manager.UIManager(self.__window_size)

        pygame.font.init()
        self.__font = pygame.font.SysFont('Arial', 15)
        self.__description_font = pygame.font.SysFont('Arial', 25, italic=True)
        self.__note_font = pygame.font.SysFont('Arial', 13, italic=True)

        self.status = description
        self.ready = False
        self.generated = 0

        self.widgets = {}
        for i in widget_list:
            self.widgets[i.name] = (i, create_widget(i, self.__manager))

        self.__generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.__window_size[0] // 2 - 150, self.__window_size[1] - 60, 300, 50),
            manager=self.__manager,
            text='СГЕНЕРИРОВАТЬ'
        )
        self.__generate_button.is_enabled = self.ready

    def __check_integers(self):
        for i in self.widgets:
            if not self.widgets[i][1].is_focused and self.widgets[i][0].type_ == 'number':
                numbers = re.findall(r'-?\d*\.\d+|-?\d+', self.widgets[i][1].get_text())
                if numbers:
                    self.widgets[i][1].set_text(numbers[0])
                else:
                    self.widgets[i][1].set_text('0')

    def __check_sliders(self):
        for i in self.widgets:
            if self.widgets[i][0].type_ == 'slider':
                a = self.widgets[i][1]
                if not a.is_focused and not a.left_button.is_focused and not a.right_button.is_focused:
                    a.set_current_value(a.get_current_value())

    def __draw_labels(self):
        label = self.__description_font.render(self.status, True, (0, 0, 0))
        self.__screen.blit(label, label.get_rect(midtop=(self.__window_size[0] // 2, 30)))

        label = self.__note_font.render('задания сохранены %d раз(а)' % self.generated, True,
                                        (0, 0, 0))
        self.__screen.blit(label,
                           label.get_rect(topleft=(self.__window_size[0] // 2 + 170, self.__window_size[1] - 50)))

        for i in self.widgets:
            label = self.__font.render(self.widgets[i][0].description, True, (0, 0, 0))
            self.__screen.blit(label, label.get_rect(bottomleft=self.widgets[i][0].relative_rect.topleft))

            if self.widgets[i][1].is_focused:
                label = self.__note_font.render('изменения не сохранены', True, (0, 0, 0))
                self.__screen.blit(label, label.get_rect(topleft=self.widgets[i][0].relative_rect.topright))

            if self.widgets[i][0].type_ == 'slider':
                label = self.__note_font.render(str(self.widgets[i][1].get_current_value()), True, (0, 0, 0))
                self.__screen.blit(label, label.get_rect(topleft=self.widgets[i][0].relative_rect.bottomleft))

    def __get_params(self):
        answer = {}
        for i in self.widgets:
            if not self.widgets[i][1].is_focused:
                type_ = self.widgets[i][0].type_
                if type_ == 'text' or type_ == 'number':
                    answer[i] = self.widgets[i][1].get_text()
                elif type_ == 'radio_list':
                    answer[i] = self.widgets[i][1].get_single_selection()
                elif type_ == 'check_list':
                    answer[i] = self.widgets[i][1].get_multi_selection()
                elif type_ == 'slider':
                    answer[i] = self.widgets[i][1].get_current_value()
        return answer

    def set_params(self, widget_list: typing.List[P]):
        params = self.__get_params()

        for i in self.widgets:
            self.widgets[i][1].kill()

        self.widgets = {}
        for i in widget_list:
            self.widgets[i.name] = (i, create_widget(i, self.__manager))
        self.ready = False

        for i in params:
            if i in self.widgets:
                if self.widgets[i][0].type_ in ['number', 'text']:
                    self.widgets[i][1].set_text(params[i])
                elif self.widgets[i][0].type_ == 'radio_list':
                    sl = self.widgets[i][1]
                    il = [i['text'] for i in sl.item_list]
                    event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                  'ui_element': sl.item_list_container.elements[sl.item_list.index(params[i])]}
                    press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                    self.__manager.process_events(press_list_item_event)
                elif self.widgets[i][0].type_ == 'check_list':
                    sl = self.widgets[i][1]
                    il = [i['text'] for i in sl.item_list]
                    for z in params[i]:
                        event_data = {'user_type': pygame_gui.UI_BUTTON_PRESSED,
                                      'ui_element': sl.item_list_container.elements[il.index(z)]}
                        press_list_item_event = pygame.event.Event(pygame.USEREVENT, event_data)
                        self.__manager.process_events(press_list_item_event)
                elif self.widgets[i][0].type_ == 'slider':
                    self.widgets[i][1].set_current_value(params[i])

    def tick(self):
        self.__generate_button.is_enabled = self.ready
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.__generate_button:
                        return 'Generate'
            self.__manager.process_events(event)

        for i in self.widgets:
            if self.widgets[i][0].type_ == 'check_list' or self.widgets[i][0].type_ == 'radio_list':
                self.widgets[i][1].unfocus()

        self.__check_integers()
        self.__check_sliders()
        self.__manager.update(0.01)
        self.__screen.fill('#f0f0f0')
        self.__draw_labels()
        self.__manager.draw_ui(self.__screen)
        pygame.display.update()

        return self.__get_params()
