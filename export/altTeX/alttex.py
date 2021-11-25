import pygame
from math import *

pygame.init()


def get_brackets(text,
                 ind):  # Вункция, находящая текст в скобках. text - текст, ind - позиция открывающей скобки. Возвращает позиции начала и конца нужной строки.
    cnt = 0
    for i in range(ind, len(text)):
        if text[i] == '(' and (i == 0 or text[i - 1] != '\\'):
            cnt += 1
        elif text[i] == ')' and (i == 0 or text[i - 1] != '\\'):
            cnt -= 1
        if cnt == 0:
            return [ind + 1, i]


def get_args(text, n,
             prev=0):  # Берёт первые n аргументов в скобках. text - текст, n - кол-во аргументов, prev - позиция открывающей скобки первого аргумента.
    answ = []
    for i in range(n):
        brack = get_brackets(text, prev)
        answ.append(text[brack[0]: brack[1]])
        prev = brack[1] + 1
    return answ


def get_brackets_reverse(text, ind):  # То же самое, что и get_brackets, но по позиции закрывающей скобки.
    cnt = 0
    for i in range(ind, 0, -1):
        if text[i] == '(':
            cnt += 1
        elif text[i] == ')':
            cnt -= 1
        if cnt == 0:
            return [i + 1, ind]


def combine(left, right):  # "Склеить" изображения (совмещение по центру)
    hght = max(left.get_height(), right.get_height())
    scr = pygame.Surface([left.get_width() + right.get_width() + 1, hght])
    scr.fill([255] * 3)
    scr.blit(left, [0, (hght - left.get_height()) // 2])
    scr.blit(right, [left.get_width() + 1, (hght - right.get_height()) // 2])
    scr.set_colorkey([255] * 3)
    return scr


def draw_figure(scr, rect, width, flipped=False):
    radius = rect[2] // 2
    img = pygame.Surface(rect[2:])
    img.fill([255] * 3)
    pygame.draw.line(img, [0] * 3, [radius, radius - 2], [radius, rect[3] // 2 - radius + 1], width=width)
    pygame.draw.line(img, [0] * 3, [radius, rect[3] // 2 + radius], [radius, rect[3] - 0 - radius], width=width)
    pygame.draw.arc(img, [0] * 3, [radius - width // 2 + 1, 0, radius * 2, radius * 2], radians(90), radians(180),
                    width=width)
    pygame.draw.arc(img, [0] * 3, [radius - width // 2 + 1, rect[3] - 1 - radius * 2, radius * 2, radius * 2],
                    radians(180), radians(270), width=width)
    pygame.draw.arc(img, [0] * 3, [-radius + width // 2 + 0, rect[3] // 2, radius * 2, radius * 2], radians(0),
                    radians(90), width=width)
    pygame.draw.arc(img, [0] * 3, [-radius + 0 + width // 2, rect[3] // 2 - radius * 2, radius * 2, radius * 2],
                    radians(270), radians(360), width=width)
    if flipped:
        img = pygame.transform.flip(img, True, False)
    img.set_colorkey([255] * 3)
    scr.blit(img, rect[:2])


def render_math(text,
                fsize=15):  # Рендер сктроки с математикой. text - строка, содержащая математику, fsize - размер шрифта
    try:
        fnt = pygame.font.SysFont('serif', fsize, italic=True)
        width = 1 + fsize // 20
        if text == '':  # Костыль 1: Если на вход подаётся пустая строка, то возвращается surface нулевого размера
            return pygame.Surface([0, 0])
        elif text.find('|') == 0:  # Обыкновенная дробь
            ut, dt = get_args(text, 2, 1)
            up = render_math(ut, fsize)
            down = render_math(dt, fsize)
            wdth = max(up.get_width(), down.get_width())
            scr = pygame.Surface([wdth + 2, up.get_height() + down.get_height() + 1 + width * 2])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2 + 1, 0])
            scr.blit(down, [(wdth - down.get_width()) // 2, up.get_height() + 2 + width])
            pygame.draw.line(scr, [0] * 3, [0, up.get_height() + 1], [wdth, up.get_height() + 1], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('chemn') == 0:  # Обозначение необратимой химической реакции
            ut, dt = get_args(text, 2, 5)
            # print(ut, dt)
            up = render_math(ut, fsize)
            down = render_math(dt, fsize)
            wdth = max(up.get_width(), down.get_width())
            hght = max(up.get_height(), down.get_height())
            scr = pygame.Surface([wdth + 2, hght * 2 + width * 3])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2 + 1, hght - up.get_height()])
            scr.blit(down, [(wdth - down.get_width()) // 2, hght + width * 3])
            pygame.draw.line(scr, [0] * 3, [0, hght + width * 0], [wdth, hght + width * 0], width=width)
            pygame.draw.line(scr, [0] * 3, [wdth, hght + width * 0], [wdth - width * 3, hght + width * -1], width=width)
            pygame.draw.line(scr, [0] * 3, [wdth, hght + width * 0], [wdth - width * 3, hght + width * 1], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('chemo') == 0:  # Обозначение обратимой химической реакции
            ut, dt = get_args(text, 2, 5)
            # print(ut, dt)
            up = render_math(ut, fsize)
            down = render_math(dt, fsize)
            wdth = max(up.get_width(), down.get_width())
            hght = max(up.get_height(), down.get_height())
            scr = pygame.Surface([wdth + 2, hght * 2 + width * 3])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2 + 1, hght - up.get_height()])
            scr.blit(down, [(wdth - down.get_width()) // 2, hght + width * 3])
            pygame.draw.line(scr, [0] * 3, [0, hght + width * -1], [wdth, hght + width * -1], width=width)
            pygame.draw.line(scr, [0] * 3, [wdth, hght + width * -1], [wdth - width * 3, hght + width * -2],
                             width=width)
            pygame.draw.line(scr, [0] * 3, [0, hght + width * 1], [wdth, hght + width * 1], width=width)
            pygame.draw.line(scr, [0] * 3, [0, hght + width * 1], [width * 3, hght + width * 2], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('img') == 0:
            name, alignment = get_args(text, 2, 3)
            alignment = alignment == 'T'
            img = pygame.image.load(name)
            if alignment:
                K = fsize / img.get_height()
                img = pygame.transform.scale(img, [int(img.get_width() * K), fsize])
            return img
        elif text.find('ir') == 0:  # Индексы (верхний и нижний) (правосторонние)
            ut, dt = get_args(text, 2, 2)
            up = render_math(ut, fsize // 2)
            down = render_math(dt, fsize // 2)
            wdth = max(up.get_width(), down.get_width())
            hght = max(up.get_height(), down.get_height())
            scr = pygame.Surface([wdth + 2, fsize // 5 + hght * 2])
            scr.fill([255] * 3)
            scr.blit(up, [scr.get_width() - up.get_width(), hght - up.get_height()])
            scr.blit(down, [scr.get_width() - down.get_width(), hght + fsize // 5])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('i') == 0:  # Индексы (верхний и нижний)
            ut, dt = get_args(text, 2, 1)
            up = render_math(ut, fsize // 2)
            down = render_math(dt, fsize // 2)
            wdth = max(up.get_width(), down.get_width())
            hght = max(up.get_height(), down.get_height())
            scr = pygame.Surface([wdth + 2, fsize // 5 + hght * 2])
            scr.fill([255] * 3)
            scr.blit(up, [0, hght - up.get_height()])
            scr.blit(down, [0, hght + fsize // 5])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('E') == 0:  # Сумма последовательности (знак СИГМА)
            ut, dt = get_args(text, 2, 1)
            up = render_math(ut, fsize // 3)
            down = render_math(dt, fsize // 3)
            centre = render_math('t(∑)', int(fsize * 1.5))
            wdth = max([up.get_width(), down.get_width(), centre.get_width()])
            scr = pygame.Surface(
                [wdth, up.get_height() + down.get_height() + centre.get_height() - int(1.5 * fsize // 5)])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2, 0])
            scr.blit(centre, [(wdth - centre.get_width()) // 2, up.get_height() - fsize // 5])
            scr.blit(down,
                     [(wdth - down.get_width()) // 2, up.get_height() + centre.get_height() - int(1.5 * fsize // 5)])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('P') == 0:  # Произведение последовательности (знак ПИ (заглавная))
            ut, dt = get_args(text, 2, 1)
            up = render_math(ut, fsize // 3)
            down = render_math(dt, fsize // 3)
            centre = render_math('t(∏)', int(fsize * 1.5))
            wdth = max([up.get_width(), down.get_width(), centre.get_width()])
            scr = pygame.Surface(
                [wdth, up.get_height() + down.get_height() + centre.get_height() - int(1.5 * fsize // 5)])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2, 0])
            scr.blit(centre, [(wdth - centre.get_width()) // 2, up.get_height() - fsize // 5])
            scr.blit(down,
                     [(wdth - down.get_width()) // 2, up.get_height() + centre.get_height() - int(1.5 * fsize // 5)])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('S') == 0:  # Интеграл
            ut, dt = get_args(text, 2, 1)
            up = render_math(ut, fsize // 3)
            down = render_math(dt, fsize // 3)
            centre = render_math('t(∫)', int(fsize * 1.5))
            wdth = max([up.get_width(), down.get_width(), centre.get_width()])
            scr = pygame.Surface([wdth, up.get_height() + down.get_height() + centre.get_height()])
            scr.fill([255] * 3)
            scr.blit(up, [(wdth - up.get_width()) // 2, 0])
            scr.blit(centre, [(wdth - centre.get_width()) // 2, up.get_height()])
            scr.blit(down, [(wdth - down.get_width()) // 2, up.get_height() + centre.get_height()])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('t') == 0:  # Рендер текста
            txt = get_args(text, 1, 1)[0].replace('\\', '')
            render = fnt.render(txt, True, [0] * 3)
            scr = pygame.Surface([render.get_width(), render.get_height()])
            scr.fill([255] * 3)
            scr.blit(fnt.render(txt, True, [0] * 3), [0, 0])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('T') == 0:  # Рендер текста заданного размера
            num = ''
            for i in range(1, len(text)):
                if text[i] in '1234567890':
                    num += text[i]
                else:
                    break
            num = int(num)
            txt = get_args(text, 1, 2 + len(str(num)))[0].replace('\\', '')
            font = pygame.font.SysFont('serif', num, italic=True)
            render = font.render(txt, True, [0] * 3)
            scr = pygame.Surface([render.get_width(), render.get_height()])
            scr.fill([255] * 3)
            scr.blit(font.render(txt, True, [0] * 3), [0, 0])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('c') == 0:  # Комбинация двух элементов (они просто ставятся рядом)
            lt, rt = get_args(text, 2, 1)
            left = render_math(lt, fsize)
            right = render_math(rt, fsize)
            hght = max(left.get_height(), right.get_height())
            scr = pygame.Surface([left.get_width() + right.get_width() + 1, hght])
            scr.fill([255] * 3)
            scr.blit(left, [0, (hght - left.get_height()) // 2])
            scr.blit(right, [left.get_width() + 1, (hght - right.get_height()) // 2])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('sqrt') == 0:  # Квадратный корень
            txt = get_args(text, 1, 4)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface(
                [math.get_width() + fsize // 3 + fsize // 15 + width, math.get_height() + fsize // 15 + width])
            scr.fill([255] * 3)
            scr.blit(math, [fsize // 3 + fsize // 15 + width, fsize // 15 + width])
            pygame.draw.line(scr, [0] * 3, [0, int((math.get_height() + 2) * 0.8)],
                             [(fsize // 3) // 2, (math.get_height() + 2)], width=width)
            pygame.draw.line(scr, [0] * 3, [(fsize // 3) // 2, (math.get_height() + 2)], [fsize // 3, 0], width=width)
            pygame.draw.line(scr, [0] * 3, [fsize // 3, 0], [scr.get_width(), 0], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('abs') == 0:  # Модуль
            txt = get_args(text, 1, 3)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface([math.get_width() + 4 + width * 3, math.get_height()])
            scr.fill([255] * 3)
            scr.blit(math, [width * 2, 1])
            pygame.draw.line(scr, [0] * 3, [0, 0], [0, (math.get_height()) - width], width=width)
            pygame.draw.line(scr, [0] * 3, [math.get_width() + width * 3, 0],
                             [math.get_width() + width * 3, (math.get_height()) - width], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('brack') == 0:  # Круглые скобки
            render = render_math(get_args(text, 1, 5)[0], fsize)
            return combine(render_math('t(\()', render.get_height()),
                           combine(render, render_math('t(\))', render.get_height())))
        elif text.find('V') == 0:  # Обозначение вектора над элементом
            txt = get_args(text, 1, 1)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface([math.get_width() + 2, math.get_height() + ceil(fsize * 0.3 / 5)])
            scr.fill([255] * 3)
            scr.blit(math, [1, ceil(fsize * 0.3 / 5)])
            pygame.draw.line(scr, [0] * 3, [0, ceil(fsize * 0.5 / 5)], [math.get_width() + 2, ceil(fsize * 0.5 / 5)],
                             width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('u') == 0:  # Подчёркивание элемента
            txt = get_args(text, 1, 1)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface([math.get_width() + 2, math.get_height() - ceil(fsize * 0.6 / 5)])
            scr.fill([255] * 3)
            scr.blit(math, [1, 0])
            pygame.draw.line(scr, [0] * 3, [0, scr.get_height() - width // 2],
                             [math.get_width() + 2, scr.get_height() - width // 2], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('pp') == 0:  # Производная 2-го порядка
            txt = get_args(text, 1, 2)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface([math.get_width() + 2, math.get_height() + ceil(fsize * 0.3 / 5)])
            scr.fill([255] * 3)
            scr.blit(math, [1, ceil(fsize * 0.3 / 5)])
            pygame.draw.circle(scr, [0] * 3, [(math.get_width() + 2) // 3, ceil(width)], ceil(width / 2))
            pygame.draw.circle(scr, [0] * 3, [2 * (math.get_width() + 2) // 3, ceil(width)], ceil(width / 2))
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('p') == 0:  # Производная 1-го порядка
            txt = get_args(text, 1, 1)[0]
            math = render_math(txt, fsize)
            scr = pygame.Surface([math.get_width() + 2, math.get_height() + ceil(fsize * 0.3 / 5)])
            scr.fill([255] * 3)
            scr.blit(math, [1, ceil(fsize * 0.3 / 5)])
            pygame.draw.circle(scr, [0] * 3, [(math.get_width() + 2) // 2, ceil(width)], ceil(width / 2))
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('O') == 0:  # Скобка систем уравнений "ИЛИ"
            num = ''
            for i in range(1, len(text)):
                if text[i] in '1234567890':
                    num += text[i]
                else:
                    break
            num = int(num)
            args = get_args(text, num, 2 + len(str(num)))
            renders = []
            sy = 0
            sx = 0
            positions = []
            for arg in args:
                positions.append(sy)
                renders.append(render_math(arg, fsize))
                sy += renders[-1].get_height() + 2
                sx = max(sx, renders[-1].get_width())
            scr = pygame.Surface([sx + 4, sy + 2])
            scr.fill([255] * 3)
            for i in range(len(args)):
                scr.blit(renders[i], [4, positions[i] + 4])
            pygame.draw.line(scr, [0] * 3, [0, 0], [0, scr.get_height()], width=width)
            pygame.draw.line(scr, [0] * 3, [0, 0], [fsize // 5, 0], width=width)
            pygame.draw.line(scr, [0] * 3, [0, scr.get_height() - 1], [fsize // 5, scr.get_height() - 1], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('A') == 0:  # Скобка систем уравнений "И"
            num = ''
            for i in range(1, len(text)):
                if text[i] in '1234567890':
                    num += text[i]
                else:
                    break
            num = int(num)
            args = get_args(text, num, 2 + len(str(num)))
            renders = []
            sy = 0
            sx = 0
            positions = []
            for arg in args:
                positions.append(sy)
                renders.append(render_math(arg, fsize))
                sy += renders[-1].get_height() + 2
                sx = max(sx, renders[-1].get_width())
            N = 3
            scr = pygame.Surface([sx + fsize // N + width, sy + 2])
            scr.fill([255] * 3)
            for i in range(len(args)):
                scr.blit(renders[i], [fsize // N + width, positions[i] + 4])
            # pygame.draw.line(scr, [0] * 3, [fsize // N, fsize // N - 2], [fsize // N, scr.get_height() // 2 - fsize // N + 1], width=width)
            # pygame.draw.line(scr, [0] * 3, [fsize // N, scr.get_height() // 2 + fsize // N], [fsize // N, scr.get_height() - 0 - fsize // N], width=width)
            # pygame.draw.arc(scr, [0] * 3, [fsize // N - width // 2 + 2, 0, fsize * 2 // N, fsize * 2 // N], radians(90), radians(180), width=width)
            # pygame.draw.arc(scr, [0] * 3, [fsize // N - width // 2 + 2, scr.get_height() - 1 - fsize * 2 // N, fsize * 2 // N, fsize * 2 // N], radians(180), radians(270), width=width)
            # pygame.draw.arc(scr, [0] * 3, [-fsize // N + width // 2 + 0, scr.get_height() // 2, fsize * 2 // N, fsize * 2 // N], radians(0), radians(90), width=width)
            # pygame.draw.arc(scr, [0] * 3, [-fsize // N + 0 + width // 2, scr.get_height() // 2 - fsize * 2 // N, fsize * 2 // N, fsize * 2 // N], radians(270), radians(360), width=width)
            draw_figure(scr, [0, 0, min(2 * fsize // N, (num - 1) * fsize // N), scr.get_height()], width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('C') == 0:  # Комбинация ряда объектов
            num = ''
            for i in range(1, len(text)):
                if text[i] in '1234567890':
                    num += text[i]
                else:
                    break
            num = int(num)
            args = get_args(text, num, 2 + len(str(num)))
            # print(args)
            if num == 2:
                return render_math('c(' + args[0] + ')(' + args[1] + ')', fsize)
            else:
                return render_math('c(' + args[0] + ')(C' + str(num - 1) + 'C' + ''.join(
                    ['(' + args[x] + ')' for x in range(1, num)]) + ')', fsize)
        elif text.find('*') == 0:  # Скалярное произведение
            scr = pygame.Surface([width * 2, width * 2])
            scr.fill([255] * 3)
            pygame.draw.circle(scr, [0] * 3, [width] * 2, width)
            return scr
        elif text.find('x') == 0:  # Векторное произведение
            scr = pygame.Surface([fsize // 3] * 2)
            scr.fill([255] * 3)
            pygame.draw.line(scr, [0] * 3, [1, 1], [fsize // 3] * 2, width)
            pygame.draw.line(scr, [0] * 3, [0, fsize // 3], [fsize // 3, 0], width)
            return scr
        elif text.find('MO') == 0:  # Матрица с квадратными скобками
            numx = ''
            for i in range(2, len(text)):
                if text[i] in '1234567890':
                    numx += text[i]
                else:
                    break
            numx = int(numx)
            numy = ''
            for i in range(3 + len(str(numx)), len(text)):
                if text[i] in '1234567890':
                    numy += text[i]
                else:
                    break
            numy = int(numy)
            args = get_args(text, numx * numy, 4 + len(str(numx)) + len(str(numy)))
            # print(args)
            renders = [[] for x in range(numy)]
            sy = 0
            sx = 0
            for i, arg in enumerate(args):
                renders[i // numx].append(render_math(arg, fsize))
                sy = max(sy, renders[i // numx][-1].get_height())
                sx = max(sx, renders[i // numx][-1].get_width())
            scr = pygame.Surface([sx * numx + width * 6, sy * numy + width * 6])
            scr.fill([255] * 3)
            for i in range(numy):
                for j in range(numx):
                    scr.blit(renders[i][j], [width * 2 + j * sx + (sx - renders[i][j].get_width()) // 2,
                                             width * 2 + i * sy + (sy - renders[i][j].get_height()) // 2])
            pygame.draw.line(scr, [0] * 3, [0, 0], [0, scr.get_height()], width=width)
            pygame.draw.line(scr, [0] * 3, [0, 0], [fsize // 5, 0], width=width)
            pygame.draw.line(scr, [0] * 3, [0, scr.get_height() - 1], [fsize // 5, scr.get_height() - 1], width=width)
            pygame.draw.line(scr, [0] * 3, [scr.get_width() - width, 0], [scr.get_width() - width, scr.get_height()],
                             width=width)
            pygame.draw.line(scr, [0] * 3, [scr.get_width() - width, 0], [scr.get_width() - width - fsize // 5, 0],
                             width=width)
            pygame.draw.line(scr, [0] * 3, [scr.get_width() - width, scr.get_height() - 1],
                             [scr.get_width() - width - fsize // 5, scr.get_height() - 1], width=width)
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('MN') == 0:  # Матрица без скобок
            numx = ''
            for i in range(2, len(text)):
                if text[i] in '1234567890':
                    numx += text[i]
                else:
                    break
            numx = int(numx)
            numy = ''
            for i in range(3 + len(str(numx)), len(text)):
                if text[i] in '1234567890':
                    numy += text[i]
                else:
                    break
            numy = int(numy)
            args = get_args(text, numx * numy, 4 + len(str(numx)) + len(str(numy)))
            # print(args)
            renders = [[] for x in range(numy)]
            sy = 0
            sx = 0
            for i, arg in enumerate(args):
                renders[i // numx].append(render_math(arg, fsize))
                sy = max(sy, renders[i // numx][-1].get_height())
                sx = max(sx, renders[i // numx][-1].get_width())
            scr = pygame.Surface([sx * numx, sy * numy])
            scr.fill([255] * 3)
            for i in range(numy):
                for j in range(numx):
                    scr.blit(renders[i][j], [j * sx + (sx - renders[i][j].get_width()) // 2,
                                             i * sy + (sy - renders[i][j].get_height()) // 2])
            scr.set_colorkey([255] * 3)
            return scr
        elif text.find('MA') == 0:  # Матрица с фигурными скобками
            numx = ''
            for i in range(2, len(text)):
                if text[i] in '1234567890':
                    numx += text[i]
                else:
                    break
            numx = int(numx)
            numy = ''
            for i in range(3 + len(str(numx)), len(text)):
                if text[i] in '1234567890':
                    numy += text[i]
                else:
                    break
            numy = int(numy)
            args = get_args(text, numx * numy, 4 + len(str(numx)) + len(str(numy)))
            # print(args)
            renders = [[] for x in range(numy)]
            sy = 0
            sx = 0
            for i, arg in enumerate(args):
                renders[i // numx].append(render_math(arg, fsize))
                sy = max(sy, renders[i // numx][-1].get_height())
                sx = max(sx, renders[i // numx][-1].get_width())
            scr = pygame.Surface([sx * numx + width * 10, sy * numy + width * 4])
            scr.fill([255] * 3)
            for i in range(numy):
                for j in range(numx):
                    scr.blit(renders[i][j], [width * 5 + j * sx + (sx - renders[i][j].get_width()) // 2,
                                             width * 2 + i * sy + (sy - renders[i][j].get_height()) // 2])

            N = 3
            draw_figure(scr, [0, 0, fsize // N, scr.get_height()], width)
            draw_figure(scr, [scr.get_width() - fsize // N, 0, fsize // N, scr.get_height()], width, flipped=True)
            scr.set_colorkey([255] * 3)
            return scr
        return pygame.Surface([0] * 2)
    except Exception as E:  # В случае ошибки напечатать подстроку, в которой возникла ошибка и вернуть красный квадрат нужного размера.
        print('ERROR with:', text)
        print(E)
        scr = pygame.Surface([fsize] * 2)
        scr.fill([255, 0, 0])
        return scr
