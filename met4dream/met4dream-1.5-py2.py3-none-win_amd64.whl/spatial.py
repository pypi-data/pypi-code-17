# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 12:46:31 2017

@author: oaarne
"""

import pyproj as pe

# spatial reference and helper functions
class geometry:

    def __init__(self, location):
        self.location = location

    def projection(self):
        proj4_str_stereographic = '+proj=stere +lat_0=90 +lon_0=70 +lat_ts=60 +units=m +a=6.371e+06 +e=0 +no_defs'
        return pe.Proj(proj4_str_stereographic)

    def get_extent(self, xmin, ymin, xmax, ymax):
        return { 'xmin': self.tint(xmin), 'ymin': self.tint(ymin), 'xmax': self.tint(xmax), 'ymax': self.tint(ymax) }

    def define_extent(self, radius):
        area = self.location
        if len(area) == 2: # assume point
            point = { 'lon': float(area[0]), 'lat': float(area[1]) }
            bbox = self.create_extent(point, radius)
        else: # assume extent
            bounds = { 'lonW': float(area[0]), 'latS': float(area[1]), 'lonE': float(area[2]), 'latN': float(area[3]) }
            bbox = self.project_extent(bounds)
        return bbox

    def project_extent(self, extent):
        lonW, latS, lonE, latN = extent['lonW'], extent['latS'], extent['lonE'], extent['latN']
        p = self.projection()
        x1, y1 = p(lonW, latS)
        x2, y2 = p(lonW, latN)
        x3, y3 = p(lonE, latN)
        x4, y4 = p(lonE, latS)

        # define extent as minimum bounding rectangle
        xmin, ymin = min(x1, x2, x3, x4), min(y1, y2, y3, y4)
        xmax, ymax = max(x1, x2, x3, x4), max(y1, y2, y3, y4)
        return self.get_extent(xmin, ymin, xmax, ymax)

    def create_extent(self, point, radius):
        lon, lat = point['lon'], point['lat']
        p = self.projection()
        x, y = p(lon, lat)

        # define extent as a square bounding box
        xmin, ymin = x - radius, y - radius
        xmax, ymax = x + radius, y + radius
        return self.get_extent(xmin, ymin, xmax, ymax)

    def tint(self, n):
        return int(round(n, 0))
