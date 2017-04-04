"""Definitions of computational geometric functions.

Delaunator: geometry namespace
https://github.com/Aluriak/Delaunator/blob/master/delaunator/libdelaunator_src/geometry.h

The geometry module assume that Y axis IS NOT inverted,
following the habitual mathematical conventions.

"""


from math import sqrt
from pydelaunator.commons import sliding

EPSILON = 0.01


def point_collide_segment(px, py, x1, y1, x2, y2) -> bool:
    return square_distance_between_segment_and_point(x1, y1, x2, y2, px, py) < EPSILON

def point_collide_point(ax, ay, bx, by) -> bool:
    return square_distance_between_points(ax, ay, bx, by) < EPSILON

def square_distance_between_segment_and_point(x1, y1, x2, y2, x, y) -> float:
    p1_p2_square_dist = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    dotProduct = ((x - x1)*(x2 - x1) + (y - y1)*(y2 - y1)) / p1_p2_square_dist
    if dotProduct < 0:
        return (x - x1)*(x - x1) + (y - y1)*(y - y1)
    elif dotProduct <= 1:
        p_p1_squareLength = (x1 - x)*(x1 - x) + (y1 - y)*(y1 - y)
        return p_p1_squareLength - dotProduct * dotProduct * p1_p2_square_dist
    return (x - x2)*(x - x2) + (y - y2)*(y - y2)

def distance_between_points(ax, ay, bx, by) -> float:
    return sqrt(square_distance_between_points(ax, ay, bx, by))

def square_distance_between_points(ax:int, ay:int, bx:int, by:int) -> int:
    return (ax - bx) ** 2 + (ay - by) ** 2

def point_in_circumcircle_of(v1:tuple, v2:tuple, v3:tuple, point:tuple) -> bool:
    """True if given position is in the circumcircle of the triangle
    formed by the 3 given vertices.

    If the three vertices are aligned, False is returned.
    Algorithm found here: https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms

    matrix:

        A B C
        D E F
        G H I

    Translate in:

    A, B, C = p1x - px,     p1y - py,    (p1x*p1x-px*px) + (p1y*p1y-py*py)
    D, E, F = p2x - px,     p2y - py,    (p2x*p2x-px*px) + (p2y*p2y-py*py)
    G, H, I = p3x - px,     p3y - py,    (p3x*p3x-px*px) + (p3y*p3y-py*py)

    determinant: AEI + BFG + CDH - AFH - BDI - CEG

    If determinant is < 0, p is in circumcircle of t.
    Consider that Y axis IS NOT inverted.

    """

    # change the data if necessary
    points = (v1, v2, v3)
    # print('CIRCLE:', *map(str, points))
    # print('CLOCKWISE:', point_in_clockwise_order(points))
    # print('COUNTER CLOCKWISE:', point_in_counter_clockwise_order(points))
    assert point_in_counter_clockwise_order(points) != point_in_clockwise_order(points)

    if not point_in_counter_clockwise_order(points):
        assert point_in_clockwise_order(points)
        v1, v2, v3 = v1, v3, v2
        points = (v1, v2, v3)
        if point_in_clockwise_order(points):  # points are aligned
            return False  # no circumcircle for aligned points, so no vertex in it
    assert point_in_counter_clockwise_order(points)

    p1x, p1y = v1
    p2x, p2y = v2
    p3x, p3y = v3
    px, py = point

    A, B, C = p1x - px,     p1y - py,    (p1x*p1x-px*px) + (p1y*p1y-py*py)
    D, E, F = p2x - px,     p2y - py,    (p2x*p2x-px*px) + (p2y*p2y-py*py)
    G, H, I = p3x - px,     p3y - py,    (p3x*p3x-px*px) + (p3y*p3y-py*py)
    determinant = A*E*I + B*F*G + C*D*H - A*F*H - B*D*I - C*E*G

    # print('CIRCLE:', *map(str, points))
    # print('CLOCKWISE:', point_in_clockwise_order(points))
    # print('COUNTER CLOCKWISE:', point_in_counter_clockwise_order(points))
    # assert point_in_counter_clockwise_order(points) != point_in_clockwise_order(points)
    # print('AREA:', signed_polygon_area(points))
    # print('DETERMINANT:', determinant)

    assert abs(determinant) > -1.  # According to Murphy's law, it will happen.
    return determinant > 0.


def signed_polygon_area(points:iter) -> float:
    """Return area of given polygon, signed. (negativ if counterclockwise).

    coords -- vector of address of Coordinates that will be tested

    Consider that Y axis IS NOT inverted.
    See point_in_clockwise_order and point_in_counter_clockwise_order functions.

    """
    # Solution found here: http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order?rq=1
    points = tuple(points)
    if len(points) <= 2:
        raise ValueError("Zero, one or two points do not describe a polygon.")
    total = 0.

    # for one, two in sliding(points, size=2):
        # ox, oy, tx, ty = *one, *two
        # total += (tx - ox) * (ty + oy)
    # # compute for one=last and two=first
    # (tx, ty), *_, (ox, oy) = points
    # total += (tx - ox) * (ty + oy)

    for one, two in sliding(points, size=2):
        ox, oy, tx, ty = *one, *two
        total += (ox * ty) - (oy * tx)
    # compute for one=last and two=first
    (tx, ty), *_, (ox, oy) = points
    total += (ox * ty) - (oy * tx)

    return -total / 2.


def clockwise_signed_polygon_area(signed_area:float) -> bool:
    """True iff given signed area is 0 or a signed area of a
    clockwise ordered polygon.

    signed_area -- the signed area of any polygon

    Consider that Y axis IS NOT inverted. Else, returned value is false.

    See http://stackoverflow.com/a/1165943/3077939

    """
    # Negative area is for clockwise order. (vice-versa if inverted axis)
    return signed_area >= 0.

def counter_clockwise_signed_polygon_area(signed_area:float) -> bool:
    """True iff given signed area is 0 or a signed area of a
    counter clockwise ordered polygon.

    signed_area -- the signed area of any polygon

    Consider that Y axis IS NOT inverted. Else, returned value is false

    See http://stackoverflow.com/a/1165943/3077939

    """
    return not clockwise_signed_polygon_area(signed_area)

def point_in_counter_clockwise_order(points) -> bool:
    """True iff points are stored in Counter Clockwise order.

    Consider that Y axis IS NOT inverted. Else, returned value is false.

    """
    # Solution found here: http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order?rq=1
    return counter_clockwise_signed_polygon_area(signed_polygon_area(points))

def point_in_clockwise_order(points) -> bool:
    """True iff points are stored in Clockwise order.

    Consider that Y axis IS NOT inverted. Else, returned value is false.

    """
    # Solution found here: http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order?rq=1
    return clockwise_signed_polygon_area(signed_polygon_area(points))


def segment_collides_line(o, p, a, b) -> int:
    """True if [OP] segment cross with (AB) line. Exact truthy value depends
    of the nature of collision.

    o -- position of a segment point
    p -- position of another segment point
    a -- position of a line point
    b -- position of another line point
    return -- 0: [OP] and (AB) don't cross
              1: ]OP[ cross (AB)
              2: O or P are on (AB)

    """
    (Ax, Ay), (Bx, By), (Ox, Oy), (Px, Py) = a, b, o, p
    AB_x = Bx - Ax
    AB_y = By - Ay
    AP_x = Px - Ax
    AP_y = Py - Ay
    AO_x = Ox - Ax
    AO_y = Oy - Ay
    tmp = (AB_x*AP_y - AB_y*AP_x)*(AB_x*AO_y - AB_y*AO_x)
    if(abs(tmp) < EPSILON):
        return 2  # alignment
    elif(tmp < 0.):
        return 1  # cross but no alignement
    return 0  # no collision


def segment_collides_segment(a, b, c, d) -> bool:
    """True if [AB] segment cross with [CD] segment.

    a -- position of a first segment point
    b -- position of another first segment point
    c -- position of a second segment point
    d -- position of another second segment point

    """
    return (
        bool(segment_collides_line(a, b, c, d)) and
        bool(segment_collides_line(c, d, a, b))
    )


def segment_crosses_segment(a, b, c, d) -> bool:
    """True if [AB] segment cross with [CD] segment.

    a -- position of a first segment point
    b -- position of another first segment point
    c -- position of a second segment point
    d -- position of another second segment point

    A crossing is a collision where there is no 3 points aligned.

    """
    return (
        segment_collides_line(a, b, c, d) == 1 and
        segment_collides_line(c, d, a, b) == 1
    )
