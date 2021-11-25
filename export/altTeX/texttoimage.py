import pygame
import alttex
import codecs

def get_brack(text, i):  # Поиск закрывающей скобки в тексте по позиции открывающей скобки
    j = text[i:].find('}')
    return i, i + j

def text_to_image(text, page_size=[1240, 1754], content_size = [1220, 1734]):  # Рендерер текста в массив изображений
    font_size = 30
    font_name = 'Calibri'
    bold = False
    italic = False
    underline = False
    binding = 'left'
    v_binding = 'bottom'
    flipped = False
    color = (0, 0, 0)
    font = pygame.font.SysFont(font_name, font_size)
    text = text.replace('\\{nextpage}', '\\{nextpаge}')
    pages = text.split('{nextpage}')  # Разрезание текста на страницы
    names = []
    #print(pages)
    for pnum, page in enumerate(pages):  # Проход по всем страницам
        lines = page.split('\n')  # Раздел страницы на строки
        PAGE = pygame.Surface(page_size)
        PAGE.fill([255] * 3)
        page_scr = pygame.Surface(content_size)
        page_scr.fill([255] * 3)
        global_pos = 0
        for linee in lines:  # Проход по всем строкам
            line = linee
            if len(line) == 0:
                line = ' '
            renders = []
            i = 0
            line = line.replace('\\{math}', '\\{mаth}')
            parts = line.split('{math}')  # Раздел строки на "математические" и "нематематические" части
            for i, part in enumerate(parts):  # Проход по всем частям строки
                if i % 2 == 1:
                    renders.append(alttex.render_math(part, font_size))  # В случае, если часть "математическая" отправить строку в модуль alttex и получить результат рендера
                else:
                    j = 0
                    while j < len(part):  # Проход по всем символам
                        if part[j] == '{' and (j == 0 or part[j - 1] != '\\'):  # Проверка на то, принадлежит ли символ команде
                            k = get_brack(part, j)[1]
                            com = part[j + 1 : k]
                            if com.find('font_size') == 0:
                                font_size = int(eval(com.split('=')[-1]) * page_size[0] / 600)
                            if com.find('font_name') == 0:
                                font_name = eval(com.split('=')[-1])
                            if com.find('binding') == 0:
                                binding = eval(com.split('=')[-1])
                            if com.find('bold') == 0:
                                bold = eval(com.split('=')[-1])
                            if com.find('italic') == 0:
                                italic = eval(com.split('=')[-1])
                            if com.find('underline') == 0:
                                underline = eval(com.split('=')[-1])
                            if com.find('color') == 0:
                                color = eval(com.split('=')[-1])
                            if com.find('flipped') == 0:
                                flipped = eval(com.split('=')[-1])
                            if com.find('v_binding') == 0:
                                v_binding = eval(com.split('=')[-1])
                            font = pygame.font.SysFont(font_name, font_size, bold=bold, italic=italic)
                            j = k + 1
                        else:
                            try:
                                if not (part[j] == '\\' and not (len(part) == j + 1 or part[j + 1] != '{')):  # Если символ "\" стоит перед командой, то команда игнорируется и остаётся строкой
                                    renders.append(font.render(part[j], True, color))
                                    if part[j] != ' ' and underline:
                                        pygame.draw.line(renders[-1], color, [0, renders[-1].get_height() - 1], [renders[-1].get_width(), renders[-1].get_height() - 1])
                            except pygame.error:
                                pass#rect = pygame.Surface([font_size, font_size // 2])
                            j += 1
            szx = sum([renders[x].get_width() for x in range(len(renders))] + [0])  # Определение горизонтального размера строки
            szy = max([renders[x].get_height() for x in range(len(renders))] + [0])  # Определение верикального размера строки
            scr = pygame.Surface([szx, szy])
            scr.fill([255] * 3)
            pos = 0
            for i in range(len(renders)):  # Добавление частей строки на страницу
                Y = 0
                if v_binding == 'bottom':
                    Y = szy - renders[i].get_height()
                elif v_binding == 'centre':
                    Y = (szy - renders[i].get_height()) // 2
                scr.blit(renders[i], [pos, Y])
                pos += renders[i].get_width()
            px = 0
            if binding == 'centre':
                px = (page_scr.get_width() - scr.get_width()) // 2
            elif binding == 'right':
                px = page_scr.get_width() - scr.get_width()
            if flipped:
                page_scr.blit(pygame.transform.rotate(scr, 180), [px, global_pos])
            else:
                page_scr.blit(scr, [px, global_pos])
            global_pos += scr.get_height() + int(font_size * page_size[0] / 4200)
        PAGE.blit(page_scr, [(page_size[0] - content_size[0]) // 2, (page_size[1] - content_size[1]) // 2])
        pygame.image.save(PAGE, 'page' + str(pnum) + '.bmp')  # Сохранение страницы в файл
        names.append('page' + str(pnum) + '.bmp')  # Добавление названия файла в массив имён
    return names
