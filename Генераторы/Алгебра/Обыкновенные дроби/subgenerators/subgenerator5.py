from random import randint, choice
from helpful import primes

import add_sub_subgenerator


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 15), randint(2, 15)
    elif difficulty == 2:
        return randint(2, 31) * choice((-1, 1)), randint(2, 31) * choice((-1, 1))
    elif difficulty == 3:
        return randint(2, 53) * choice((-1, 1)), randint(2, 53) * choice((-1, 1))


def get_denoms(difficulty):
    if difficulty == 1:
        primes11 = primes(11)
        a, b, c = choice(primes11), choice(primes11), choice(primes11)
        return a * b, a * c
    elif difficulty == 2:
        primes11 = primes(11)
        primes50 = primes(50)
        a, b, c = choice(primes11), choice(primes50), choice(primes50)
        return a * b, a * c
    elif difficulty == 3:
        primes11 = primes(11)
        a = choice(primes11)
        b = 1
        t = choice(primes11)
        while b * t <= 50:
            b *= t
            t = choice(primes11)
        c = 1
        t = choice(primes11)
        while c * t <= 50:
            c *= t
            t = choice(primes11)
        return a * b, a * c


def generate(params):
    return add_sub_subgenerator.generate(params, get_nums, get_denoms)
