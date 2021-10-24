from random import randint, choice
from helpful import primes

import add_sub_subgenerator


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 15), randint(2, 15)
    elif difficulty == 2:
        return randint(16, 31) * choice((-1, 1)), randint(16, 31) * choice((-1, 1))
    elif difficulty == 3:
        return randint(32, 53) * choice((-1, 1)), randint(32, 53) * choice((-1, 1))


def get_denoms(difficulty):
    if difficulty == 1:
        primes7 = primes(7)
        gcd = choice(primes7)

        a_set = set()
        a = 1
        t = choice(primes7)
        while a * t <= 10:
            a *= t
            a_set.add(t)
            t = choice(primes7)

        b_set = set(primes7) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 10:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b
    elif difficulty == 2:
        primes17 = primes(8, 17)
        gcd = choice(primes17)

        a_set = set()
        a = 1
        t = choice(primes17)
        while a * t <= 25:
            a *= t
            a_set.add(t)
            t = choice(primes17)

        b_set = set(primes17) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 25:
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
    return add_sub_subgenerator.generate(params, get_nums, get_denoms)
