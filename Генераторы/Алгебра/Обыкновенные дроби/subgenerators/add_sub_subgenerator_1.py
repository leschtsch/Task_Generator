from random import randint, seed
from fractions import Fraction

from helpful_1 import str_sign as sign


def sort_fracs(num1, denom1, num2, denom2):
    res = []
    res.extend(max((num1, denom1), (num2, denom2), key=lambda x: x[0] / x[1]))
    res.extend(min((num1, denom1), (num2, denom2), key=lambda x: x[0] / x[1]))
    return tuple(res)


def generate_task(difficulty, nums_getter, denoms_getter):
    denom1, denom2 = denoms_getter(difficulty)
    num1, num2 = nums_getter(difficulty)
    frac1, frac2 = Fraction(num1, denom1), Fraction(num2, denom2)
    if difficulty == 1:
        if randint(0, 1):
            if frac1 < frac2:
                frac1, frac2 = frac2, frac1
            frac3 = frac1 - frac2
            num3 = frac3.numerator
            denom3 = frac3.denominator
            int3 = num3 // denom3
            num3 = num3 % denom3
            task = r'\frac{%d}{%d}-\frac{%d}{%d}' % sort_fracs(num1, denom1, num2, denom2)
            answer = task + ' = '
            if int3:
                answer += str(int3)
            if num3:
                answer += r'\frac{%d}{%d}' % (num3, denom3)
            return task, answer
        else:
            frac3 = frac1 + frac2
            num3 = frac3.numerator
            denom3 = frac3.denominator
            int3 = num3 // denom3
            num3 = num3 % denom3
            task = r'\frac{%d}{%d}+\frac{%d}{%d}' % (num1, denom1, num2, denom2)
            answer = task + ' = '
            if int3:
                answer += str(int3)
            if num3:
                answer += r'\frac{%d}{%d}' % (num3, denom3)
            return task, answer
    elif difficulty == 2 or difficulty == 3:
        if randint(0, 1):
            frac3 = frac1 - frac2
            num3 = abs(frac3.numerator)
            denom3 = abs(frac3.denominator)
            int3 = num3 // denom3
            num3 = num3 % denom3
            task = r'\frac{%d}{%d}-\frac{%d}{%d}' % (num1, denom1, num2, denom2)
            answer = task + ' = ' + sign(frac3)
            if int3:
                answer += str(abs(int3))
            if num3:
                answer += r'\frac{%d}{%d}' % (abs(num3), abs(denom3))
            return task, answer
        else:
            frac3 = frac1 + frac2
            num3 = abs(frac3.numerator)
            denom3 = abs(frac3.denominator)
            int3 = num3 // denom3
            num3 = num3 % denom3
            task = r'\frac{%d}{%d}+\frac{%d}{%d}' % (num1, denom1, num2, denom2)
            answer = task + ' = ' + sign(frac3)
            if int3:
                answer += str(abs(int3))
            if num3:
                answer += r'\frac{%d}{%d}' % (abs(num3), abs(denom3))
            return task, answer


def generate(difficulty, quantity, nums_getter, denoms_getter):
    tasks, answers = [], []

    for i in range(quantity):
        task, answer = generate_task(difficulty, nums_getter, denoms_getter)
        tasks.append(task)
        answers.append(answer)
        seed(randint(0, 999999))

    return tasks, answers
