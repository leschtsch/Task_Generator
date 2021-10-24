import pygame_gui
from interface.gen_param import GeneratorParameter as P
from pygame_gui.ui_manager import UIManager


def create_widget(gen_param: 'P', manager: 'UIManager'):
    if gen_param.type_ == 'text':
        return pygame_gui.elements.UITextEntryLine(
            relative_rect=gen_param.relative_rect,
            manager=manager,
        )

    if gen_param.type_ == 'number':
        return pygame_gui.elements.UITextEntryLine(
            relative_rect=gen_param.relative_rect,
            manager=manager,
        )

    if gen_param.type_ == 'radio_list':
        return pygame_gui.elements.UISelectionList(
            relative_rect=gen_param.relative_rect,
            item_list=gen_param.options,
            manager=manager,
            allow_multi_select=False,
        )

    if gen_param.type_ == 'check_list':
        return pygame_gui.elements.UISelectionList(
            relative_rect=gen_param.relative_rect,
            item_list=gen_param.options,
            manager=manager,
            allow_multi_select=True,
        )

    '''
    drop_down_menu
    text_entry_line
    selection_list
    '''