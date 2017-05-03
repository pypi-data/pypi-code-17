# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 17:42:33 2016

@author: wtr
20170428 v 1.0 新增getdistance_list 计算一个数组的第一个点到最后一个点的距离
"""

import math

"""
 第一个参数为一个路的起点和终点组成的list,如下:
 sp=[116.291087273989,40.0484742339865]
 ep=[116.292488728211,40.0487113818083]
 lines=[sp,ep]
 第二个参数为前进了多少的百分比
"""


def line_interpolate_point(lines, percent):
    p1, p2 = lines
    # 如果传进来的数大于1
    if percent > 1:
        return 'false'
    # 如果第2个参数为0或者1
    if percent == 0:
        return p1
    if percent == 1:
        return p2
    # 计算
    return [(p2[0] - p1[0]) * percent + p1[0], (p2[1] - p1[1]) * percent + p1[1]]


#############################################################
def getDistance(start, end):
    if start == end:
        return 0
    else:
        lat1 = (math.pi / 180) * start[1]
        lat2 = (math.pi / 180) * end[1]
        lon1 = (math.pi / 180) * start[0]
        lon2 = (math.pi / 180) * end[0]
        # 地球半径
        R = 6371
        # noinspection PyBroadException
        try:
            d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * R
        except:
            print start, end
            return 0
        return d * 1000


def getDistance_list(vlist):
    dis = 0
    for i in range(len(vlist) - 1):
        dis += getDistance(vlist[i], vlist[1])
    return dis


############################################################
'''已知点A经纬度，根据B点据A点的距离，和方位，求B点的经纬度
   para a 已知点a
   para distance b到a的距离
   para angle b相对于a的方位
   return b的经纬度坐标
'''


############################################################
def getJWD(a, distance, angle):
    Rc = 6378137  # 赤道半径
    Rj = 6356725  # 极半径
    dx = distance * math.sin(angle * math.pi / 180)
    dy = distance * math.cos(angle * math.pi / 180)
    alon = float(a[0])
    alat = float(a[1])
    a_radlo = alon * math.pi / 180
    a_radla = alat * math.pi / 180
    Ec = Rj + (Rc - Rj) * (90 - alat) / 90
    Ed = Ec * math.cos(a_radla)
    blon = (dx / Ed + a_radlo) * 180 / math.pi
    blat = (dy / Ec + a_radla) * 180 / math.pi
    return [blon, blat]


"""
算点到直线的投影
"""


# 经度是x,纬度是y
def getclosedpoint(sp, ep, pt):
    # 如果纬度相同,返回线外点的经度,线上的纬度
    if sp[1] == ep[1]:
        return [pt[0], sp[1]]
    # 如果经度相同,返回线外点的纬度,线上的经度
    if sp[0] == sp[0]:
        return [sp[0], pt[1]]
    # http://blog.csdn.net/luols/article/details/7482626
    k = (sp[1] - ep[1]) / (sp[0] - ep[0])
    x = float((k * sp[0] + pt[0] / k + pt[1] - sp[1]) / (1 / k + k))
    y = float(-1 / k * (x - pt[0]) + pt[1])
    return [x, y]


def IsPointInRec(point, rec):
    sw = rec[0]
    ne = rec[1]
    return ((point[0] >= sw[0] and point[0] <= ne[0] and point[1] >= sw[1] and point[1] <= ne[1]))


def IsPointInPolygon(point, polygon, rec):
    if (not IsPointInRec(point, rec)):
        return False
    pts = polygon
    N = len(pts)
    boundOrVertex = True
    intersectCount = 0
    precision = 2e-10
    p = point
    p1 = pts[0]
    for i in range(1, N + 1):
        if p == p1:
            return boundOrVertex
        p2 = pts[i % N]
        if (p[1] < min(p1[1], p2[1])) or (p[1] > max(p1[1], p2[1])):
            p1 = p2
            continue
        if (p[1] > min(p1[1], p2[1])) and (p[1] < max(p1[1], p2[1])):
            if (p[0] <= max(p1[0], p2[0])):
                if (p1[1] == p2[1]) and (p[0] >= min(p1[0], p2[0])):
                    return boundOrVertex
                if (p1[0] == p2[0]):
                    if (p1[0] == p[0]):
                        return boundOrVertex
                    else:
                        intersectCount += 1
                else:
                    xinters = (p[1] - p1[1]) * (p2[0] - p1[0]) / \
                              (p2[1] - p1[1]) + p1[0]
                    if (abs(p[0] - xinters) < precision):
                        return boundOrVertex
                    if p[0] < xinters:
                        intersectCount += 1
        else:
            if (p[1] == p2[1]) and (p[0] <= p2[0]):
                p3 = pts[(i + 1) % N]
                if (p[1] > min(p1[1], p3[1])) and (p[1] <= max(p1[1], p3[1])):
                    intersectCount += 1
                else:
                    intersectCount += 2
        p1 = p2
    if (intersectCount % 2 == 0):
        return False
    else:
        return True


"""
算点到直线距离
"""


def getdistance_pl(sp, ep, pt):
    pro = getclosedpoint(sp, ep, pt)
    return getDistance(pro, pt)


def test_by_wtr():
    sp = [116.291087273989, 40.0484742339865]
    ep = [116.292488728211, 40.0487113818083]
    res = line_interpolate_point([sp, ep], 0.5)
    print res
