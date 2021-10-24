from pygame import Rect


class GeneratorParameter:
    def __init__(self, name, type_, relative_rect, description='', options=None):
        self.name = name
        self.type_ = type_
        self.relative_rect = Rect(relative_rect[0], relative_rect[1], relative_rect[2], relative_rect[3])
        self.options = options
        self.description = description
