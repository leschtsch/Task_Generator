from random import randint, choice
import add_sub_subgenerator_1


def get_nums(difficulty):
    if difficulty == 1:
        return randint(2, 99), randint(2, 99)
    elif difficulty == 2:
        return randint(2, 99) * choice((-1, 1)), randint(2, 99) * choice((-1, 1))
    elif difficulty == 3:
        return randint(100, 999) * choice((-1, 1)), randint(100, 999) * choice((-1, 1))


def get_denoms(difficulty):
    if difficulty == 1 or difficulty == 2:
        denom = randint(2, 99)
        return denom, denom
    elif difficulty == 3:
        denom = randint(100, 999)
        return denom, denom


def generate(params):
    return add_sub_subgenerator_1.generate(int(params['2difficulty_level']), int(params['2quantity']), get_nums,
                                         get_denoms)
