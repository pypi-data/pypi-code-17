from typing import List, Any
from math import sqrt


def l1_norm(values: List[Any]) -> float:
    return sum(map(abs, values))


def l2_norm(values: List[Any]) -> float:
    return sqrt(sum((x*x for x in values)))


def square(value: float) -> float:
    return value*value
