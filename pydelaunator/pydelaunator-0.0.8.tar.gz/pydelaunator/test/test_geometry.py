

import math
import pytest
import itertools
from pydelaunator.geometry import *


def test_distance_between_points():
    assert square_distance_between_points(0, 0, 0, 0) == 0
    assert square_distance_between_points(0, 0, 1, 1) == 2

def test_square_distance_between_segment_and_point():
    d = math.sqrt(square_distance_between_segment_and_point(0,0, 1,1, 1,2))
    assert abs(d - 1.) < EPSILON

def test_point_collide_segment():
    assert point_collide_segment(0, 50, 0, 0, 0, 100)
    assert point_collide_segment(50, 50, 100, 0, 0, 100)

def test_point_in_clockwise_order():
    points = (0, 0), (0, 50), (50, 50), (50, 0)
    assert signed_polygon_area(points) == -signed_polygon_area(reversed(points))
    assert     point_in_clockwise_order(points)
    assert not point_in_counter_clockwise_order(points)
    assert not point_in_clockwise_order(reversed(points))
    assert     point_in_counter_clockwise_order(reversed(points))

def test_point_in_clockwise_order_2():
    points = (0, 0), (50, 50), (100, 0)
    assert signed_polygon_area(points) == -signed_polygon_area(reversed(points))
    assert     point_in_clockwise_order(points)
    assert not point_in_counter_clockwise_order(points)
    assert not point_in_clockwise_order(reversed(points))
    assert     point_in_counter_clockwise_order(reversed(points))

def test_point_in_counter_clockwise_order():
    points = (0, 0), (100, 0), (50, 50)
    assert signed_polygon_area(points) == -signed_polygon_area(reversed(points))
    assert not point_in_clockwise_order(points)
    assert     point_in_counter_clockwise_order(points)
    assert     point_in_clockwise_order(tuple(reversed(points)))
    assert not point_in_counter_clockwise_order(tuple(reversed(points)))


def test_signed_polygon_area():
    points = (5,0), (6,4), (4,5), (1,5), (1,0)
    assert signed_polygon_area(points) == -22
    assert point_in_counter_clockwise_order(points)
    assert signed_polygon_area(reversed(points)) == 22
    assert point_in_clockwise_order(reversed(points))


def test_signed_polygon_area_2():
    points = (3, 4), (5, 11), (12, 8), (9, 5), (5, 6), (3, 4)
    assert signed_polygon_area(points) == 30
    assert point_in_clockwise_order(points)
    assert signed_polygon_area(reversed(points)) == -30
    assert not point_in_clockwise_order(reversed(points))


def test_point_in_circumcircle_of():
    # aligned points
    assert not point_in_circumcircle_of((1,2), (0,2), (3,2), (1,-100))
    assert not point_in_circumcircle_of((0,2), (1,2), (3,2), (2,4))
    assert not point_in_circumcircle_of((2,1), (2,0), (2,3), (2,4))

    # non aligned points
    assert not point_in_circumcircle_of((1,0), (1,2), (0,1), (3-EPSILON,1))
     # 3 firsts are in counter-clockwise
    assert     point_in_circumcircle_of((1,0), (1,2), (0,1), (2-0.1,1))
     # 3 firsts are in counter-clockwise
    assert     point_in_circumcircle_of((1,0), (1,2), (0,1), (1-EPSILON,1))

def test_point_in_circumcircle_of_more():
    assert     point_in_circumcircle_of((0, 100), (100, 100), (100, 0), (70, 10))
    assert     point_in_circumcircle_of((0, 10), (4, 4), (10, 0), (10, 10))
    assert     point_in_circumcircle_of((0, 100), (40, 40), (100, 0), (100, 100))
    assert     point_in_circumcircle_of((0, 100), (70, 10), (100, 0), (100, 100))
    assert not point_in_circumcircle_of((100, 100), (100, 0), (70, 10), (0, 100))
    assert not point_in_circumcircle_of((40, 60), (40, 40), (80, 10), (100, 100))

def test_point_exactly_on_circumcircle():
    points = (0, 100), (0, 0), (100, 0), (100, 100)
    for combi in itertools.combinations(points, r=4):
        assert not point_in_circumcircle_of(*points)


def test_segment_cross_segment():
    points = (1, 3), (3, 3), (3, 1), (3, 3)
    assert segment_collides_line(*points) == 2
    assert     segment_collides_segment(*points)
    assert not segment_crosses_segment(*points)

def test_segment_cross_segment_2():
    points = (0, 1), (1, 0), (0, 0), (1, 1)
    assert segment_collides_line(*points) == 1
    assert segment_collides_segment(*points)
    assert segment_crosses_segment(*points)

def test_segment_cross_segment_3():
    points = (0, 1), (0, 0), (1, 0), (1, 1)
    assert segment_collides_line(*points) == 0
    assert not segment_collides_segment(*points)
    assert not segment_crosses_segment(*points)

def test_segment_cross_segment_4():
    points = (0, 1), (1, 1), (0, 2), (0, 0)
    assert segment_collides_line(*points) == 2
    assert     segment_collides_segment(*points)
    assert not segment_crosses_segment(*points)

def test_segment_cross_segment_5():
    points = (262, 542), (263, 541), (503, 488), (0, 600)
    assert segment_collides_line(*points) == 1
    assert     segment_collides_segment(*points)
    assert     segment_crosses_segment(*points)
