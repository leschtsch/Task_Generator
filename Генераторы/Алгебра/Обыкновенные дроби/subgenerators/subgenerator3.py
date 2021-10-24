from random import randint, choice

from helpful import primes
import add_sub_subgenerator


def get_denoms(difficulty):
    prob = randint(0, 2)
    if difficulty == 1:
        if prob == 0:
            primes15 = primes(15)
            denom1 = choice(primes15)
            primes15.remove(denom1)
            denom2 = choice(primes15)
            return denom1, denom2
        elif prob == 1:
            denom1 = randint(2, 15)
            denom2 = denom1 + 1
            return denom1, denom2
        elif prob == 2:
            denom1 = choice([i for i in range(3, 16) if i % 2])
            denom2 = denom1 + 2
            return denom1, denom2
    elif difficulty == 2:
        if prob == 0:
            primes31 = primes(16,31)
            denom1 = choice(primes31)
            primes31.remove(denom1)
            denom2 = choice(primes31)
            return denom1, denom2
        elif prob == 1:
            denom1 = randint(16, 30)
            denom2 = denom1 + 1
            return denom1, denom2
        elif prob == 2:
            denom1 = choice([i for i in range(17, 31) if i % 2])
            denom2 = denom1 + 2
            return denom1, denom2
    elif difficulty == 3:
        if prob == 0:
            primes53 = primes(32,53)
            denom1 = choice(primes53)
            primes53.remove(denom1)
            denom2 = choice(primes53)
            return denom1, denom2
        elif prob == 1:
            denom1 = randint(31, 50)
            denom2 = denom1 + 1
            return denom1, denom2
        elif prob == 2:
            denom1 = choice([i for i in range(33, 51) if i % 2])
            denom2 = denom1 + 2
            return denom1, denom2


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 15), randint(2, 15)
    elif difficulty == 2:
        return randint(16, 30) * choice((-1, 1)), randint(16, 30) * choice((-1, 1))
    elif difficulty == 3:
        return randint(31, 50) * choice((-1, 1)), randint(31, 50) * choice((-1, 1))


def generate(params):
    return add_sub_subgenerator.generate(params, get_nums, get_denoms)
