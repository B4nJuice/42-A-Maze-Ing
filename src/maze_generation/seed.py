import random
import math


def create_seed(seed: int) -> int:
    """
    Initialize the seed for random generation.
    If seed is 0, a random seed is generated.
    :param seed: Seed to use (0 for random).
    :return: Seed used.
    """
    if seed == 0:
        seed = random.randint(1, 999999999)
    random.seed(seed)
    return seed


def next_randint(min: int, max: int):
    """
    Returns a pseudo-random integer in the interval [min, max[
    :param min: Lower bound (inclusive).
    :param max: Upper bound (exclusive).
    :return: Pseudo-random integer.
    """
    r: float = random.random()
    return math.floor(min + r * (max - min))
