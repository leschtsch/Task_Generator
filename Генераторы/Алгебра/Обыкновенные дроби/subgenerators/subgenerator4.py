from random import randint, choice

import add_sub_subgenerator


def get_denoms(difficulty):
    if difficulty == 1:
        denom1 = randint(2, 7)
        denom2 = denom1 * randint(2, 7)
        return denom1, denom2
    elif difficulty == 2:
        denom1 = randint(2, 17)
        denom2 = denom1 * randint(2, 17)
        return denom1, denom2
    elif difficulty == 3:
        denom1 = randint(2, 31)
        denom2 = denom1 * randint(2, 31)
        return denom1, denom2


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 15), randint(2, 15)
    elif difficulty == 2:
        return randint(2, 31) * choice((-1, 1)), randint(2, 31) * choice((-1, 1))
    elif difficulty == 3:
        return randint(2, 53) * choice((-1, 1)), randint(2, 53) * choice((-1, 1))


def generate(params):
    return add_sub_subgenerator.generate(params, get_nums, get_denoms)
