import random
import math


def create_seed(seed: int) -> int:
    """
    Initialize and set the RNG seed.

    If ``seed`` is 0 a new random seed is chosen and used. The function
    sets the Python RNG state via :func:`random.seed` and returns the
    seed value actually used.

    Parameters
    ----------
    seed : int
        Seed to use. If 0, a new random positive seed will be generated.

    Returns
    -------
    int
        The seed value used to initialize the RNG.
    """
    if seed == 0:
        seed = random.randint(1, 999999999)
    random.seed(seed)
    return seed


def next_randint(min: int, max: int):
    """
    Return a pseudo-random integer in the interval [min, max).

    This uses :func:`random.random` to produce a float in [0, 1) and maps
    it to the integer interval using floor.

    Parameters
    ----------
    min : int
        Inclusive lower bound.
    max : int
        Exclusive upper bound.

    Returns
    -------
    int
        Pseudo-random integer in the range [min, max).
    """
    r: float = random.random()
    return math.floor(min + r * (max - min))
