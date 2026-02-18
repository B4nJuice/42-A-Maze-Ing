import random
import math


def create_seed(seed: int) -> int:
    """Initialize the seed for random generation.

    If seed is 0, a random seed is generated from the system.
    The seed is then used to initialize Python's random module.

    Parameters
    ----------
    seed : int
        Seed to use (0 for random generation).

    Returns
    -------
    int
        The seed value that was used.
    """
    if seed == 0:
        seed = random.randint(1, 999999999)
    random.seed(seed)
    return seed


def next_randint(min: int, max: int) -> int:
    """Return a pseudo-random integer in the interval [min, max[.

    Generates a pseudo-random integer using the system's random generator,
    constrained to the specified range with inclusive lower bound and
    exclusive upper bound.

    Parameters
    ----------
    min : int
        Lower bound (inclusive).
    max : int
        Upper bound (exclusive).

    Returns
    -------
    int
        Pseudo-random integer in [min, max[.
    """
    r: float = random.random()
    return math.floor(min + r * (max - min))
