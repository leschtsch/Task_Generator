from pygame import Rect


class GeneratorParameter:
    def __repr__(self):
        return self.name

    def __init__(self, name, type_, relative_rect, description='', **kwargs):
        self.name = name
        self.type_ = type_
        self.relative_rect = Rect(relative_rect[0], relative_rect[1], relative_rect[2], relative_rect[3])
        if 'options' in kwargs:
            self.options = kwargs['options']
        if 'value_range' in kwargs:
            self.value_range = kwargs['value_range']
        self.description = description
