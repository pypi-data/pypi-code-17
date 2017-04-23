import numpy as np


def rand_lin_noise():
    beta = np.random.normal()
    return lambda x: beta * x + np.random.random(size=len(x))


def const_lin_noise(x):
    beta = np.random.normal()
    return beta * x + np.random.random(size=len(x))


def random_walk(x):
    return np.cumsum(np.random.normal(size=x.shape[0]))


def random_walk_limit(limit=2):
    vals = {"current": 0}

    def walk(value):
        new_val = np.random.normal()

        if vals["current"] >= limit:
            new_val = -abs(new_val)
        elif vals["current"] <= -limit:
            new_val = abs(new_val)

        vals["current"] += new_val
        return vals["current"]

    return walk
