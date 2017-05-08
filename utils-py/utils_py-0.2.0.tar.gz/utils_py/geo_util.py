#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <ytjia.zju@gmail.com>


def is_in_polygon(point, polygon):
    """

    :param point: (lat, lng)
    :param polygon: [point1, point2, point3, point4](points are ordered)
    :return: True if point is in the polygon else False
    """
    point_num = len(polygon)
    if point_num < 3:
        return False
    result = False
    for i in range(0, point_num):
        point_one = polygon[i]
        point_two = polygon[i - 1]
        if (point_one[0] < point[0] <= point_two[0]) or (
                        point_two[0] < point[0] <= point_one[0]):
            if (point_one[1] + (point[0] - point_one[0]) / (
                        point_two[0] - point_one[0]) * (
                        point_two[1] - point_one[1]) <
                    point[1]):
                result = not result
    return result


def polygon_trans(p):
    """

    :param p: polygon list with dict("lat: v1, "lng": v2) as elements
    :return: polygon list with (v_lat, v_lng) as elements
    """
    new_p = []
    for point in p:
        new_p.append((point["lat"], point["lng"]))
    return new_p
