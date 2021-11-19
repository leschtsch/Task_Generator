from random import randint, choice, seed
from math import gcd


def get_frac_task(num, denom, sign=''):
    if randint(0, 1):
        latex_common = sign + r'\frac{%d}{%d}' % (num, denom)
        int_ = num // denom
        num2 = num % denom
        g = gcd(num2, denom)
        num2 //= g
        denom2 = denom // g
        if num2:
            latex_mixed = sign+r'%d\frac{%d}{%d}' % (int_, num2, denom2)
        else:
            latex_mixed = sign+str(int_)
        return latex_common, latex_common + ' = ' + latex_mixed
    else:
        if not num % denom:
            num += 1
        int_ = num // denom
        num2 = num % denom
        latex_mixed = sign + r'%d\frac{%d}{%d}' % (int_, num2, denom)
        g = gcd(num, denom)
        num //= g
        denom = denom // g
        latex_common = sign + r'\frac{%d}{%d}' % (num, denom)
        return latex_mixed, latex_mixed + ' = ' + latex_common


def generate_task(difficulty):
    if difficulty == 1:
        denom = randint(2, 9)
        num = randint(denom, 99 - denom)
        return get_frac_task(num, denom)

    elif difficulty == 2:
        sign = choice(['-', ''])
        denom = randint(11, 25)
        num = randint(denom, 99 - denom)
        return get_frac_task(num, denom, sign)

    elif difficulty == 3:
        sign = choice(['-', ''])
        denom = randint(111, 256)
        num = randint(denom, 999 - denom)
        return get_frac_task(num, denom, sign)


def generate(params):
    difficulty = int(params['difficulty_level'])
    quantity = int(params['quantity'])
    tasks, answers = [], []

    for i in range(quantity):
        task, answer = generate_task(difficulty)
        tasks.append(task)
        answers.append(answer)
        seed(randint(0, 999999))

    return tasks, answers
