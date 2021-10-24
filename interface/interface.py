import pygame_gui
import pygame
from interface.gen_param import GeneratorParameter as P
from interface.widget_creator import create_widget
import typing
import re


class Interface:
    def __init__(self, window_size, widget_list: typing.List[P], description=''):
        pygame.init()
        self.__window_size = window_size
        self.__screen = pygame.display.set_mode(self.__window_size)
        self.__screen.fill('#f0f0f0')
        self.__manager = pygame_gui.ui_manager.UIManager(self.__window_size)

        pygame.font.init()
        self.__font = pygame.font.SysFont('Arial', 15)
        self.__description_font = pygame.font.SysFont('Arial', 25, italic=True)
        self.__note_font = pygame.font.SysFont('Arial', 13, italic=True)

        self.status = ''
        self.ready = False
        self.generated = 0

        self.widgets = {}
        for i in widget_list:
            self.widgets[i.name] = (i, create_widget(i, self.__manager))

        self.__generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.__window_size[0] // 2 - 150, self.__window_size[1] - 50, 300, 50),
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
                label = self.__note_font.render(' изменения не сохранены', True, (0, 0, 0))
                self.__screen.blit(label, label.get_rect(topleft=self.widgets[i][0].relative_rect.topright))

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
        return answer

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
        self.__manager.update(0.01)
        self.__screen.fill('#f0f0f0')
        self.__draw_labels()
        self.__manager.draw_ui(self.__screen)
        pygame.display.update()

        return self.__get_params()
