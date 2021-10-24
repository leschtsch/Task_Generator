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
        primes7 = primes(7)

        gcd = 1
        t = choice(primes7)
        while gcd * t <= 7:
            gcd *= t
            t = choice(primes7)

        a_set = set()
        a = 1
        t = choice(primes7)
        while a * t <= 7:
            a *= t
            a_set.add(t)
            t = choice(primes7)

        b_set = set(primes7) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 7:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b
    elif difficulty == 2:
        primes11 = primes(11)

        gcd = 1
        t = choice(primes11)
        while gcd * t <= 15:
            gcd *= t
            t = choice(primes11)

        a_set = set()
        a = 1
        t = choice(primes11)
        while a * t <= 15:
            a *= t
            a_set.add(t)
            t = choice(primes11)

        b_set = set(primes11) - a_set
        b = 1
        t = choice(list(b_set))
        while b * t <= 15:
            b *= t
            t = choice(list(b_set))

        return gcd * a, gcd * b
    elif difficulty == 3:
        primes17 = primes(17)

        gcd = 1
        t = choice(primes17)
        while gcd * t <= 125:
            gcd *= t
            t = choice(primes17)

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


def generate(params):
    return add_sub_subgenerator.generate(params, get_nums, get_denoms)
