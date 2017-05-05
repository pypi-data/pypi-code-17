from typing import Tuple


class Shape:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_points(self) -> Tuple[Tuple[float, float]]:
        p1 = self.x1, self.y1
        p2 = self.x2, self.y2
        return p1, p2

shape1 = Shape(3, 4, 3, 5)
points = shape1.get_points()
print(points)