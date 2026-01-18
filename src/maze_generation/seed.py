import random
import math


def create_seed(seed: int) -> int:
    if seed == 0:
        seed = random.randint(1, 999999999)
    random.seed(seed)
    return seed


def next_randint(min: int, max: int):
    r: float = random.random()
    return math.floor(min + r * (max - min))
