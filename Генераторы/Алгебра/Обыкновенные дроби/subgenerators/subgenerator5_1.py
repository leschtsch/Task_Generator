from random import randint, choice
from helpful_1 import primes

import add_sub_subgenerator_1


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 15), randint(2, 15)
    elif difficulty == 2:
        return randint(16, 31) * choice((-1, 1)), randint(16, 31) * choice((-1, 1))
    elif difficulty == 3:
        return randint(32, 53) * choice((-1, 1)), randint(32, 53) * choice((-1, 1))


def get_denoms(difficulty):
    if difficulty == 1:
        primes11 = primes(7)
        gcd = choice(primes11)

        a_set = set()
        a = 1
        t = choice(primes11)
        while a * t <= 10:
            a *= t
            a_set.add(t)
            t = choice(primes11)

        b_set = set(primes11) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 10:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b
    elif difficulty == 2:
        primes11 = primes(11)
        gcd = choice(primes(11))

        a_set = set()
        a = 1
        t = choice(primes11)
        while a * t <= 30:
            a *= t
            a_set.add(t)
            t = choice(primes11)

        b_set = set(primes11) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 30:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b
    elif difficulty == 3:
        primes19 = primes(19, 29)
        gcd = choice(primes19)

        a_set = set()
        a = 1
        t = choice(primes19)
        while a * t <= 35:
            a *= t
            a_set.add(t)
            t = choice(primes19)

        b_set = set(primes19) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 35:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b


def generate(params):
    return add_sub_subgenerator_1.generate(int(params['5difficulty_level']), int(params['5quantity']), get_nums, get_denoms)
