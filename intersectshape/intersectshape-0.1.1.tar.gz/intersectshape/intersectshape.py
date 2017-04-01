#!/usr/bin/env python3.6
# coding: utf-8


"""Reverse geocoding from a shapefile of polygons."""


import os
import logging
import shapefile
from shapely.geometry import shape
from shapely.geometry import Point
from intersectshape import SpatialIndex


# Log
log = logging.getLogger('intersectshape.reversegeoloc')


class ReverseGeolocException(ValueError):
    pass


class ReverseGeolocShapefile(shapefile.Reader):
    """Reverse geocoding from a shapefile of polygons."""

    def __init__(self, *args, clean_index=False, **kwargs):
        """Reverse geocoding from a shapefile of polygons.

        :param args: args of shapefile.Reader
        :param clean_index: True/False to erase existing spatial index.
        :param kwargs: kwargs of shapefile.Reader
        """
        super().__init__(*args, **kwargs)

        # Check if polygons
        if self.shapeType not in (shapefile.POLYGON,
                                  shapefile.POLYGONZ,
                                  shapefile.POLYGONM):
            log.error("shapefile geometries ares not polygons!")
            raise ReverseGeolocException("shapefile geometries are not "
                                         "polygons!")

        self.fnidx = self.shapeName + '.sidx.npy'  # spatial index filename
        self.sidx = SpatialIndex()

        # Open or create a spatialindex
        if clean_index or not os.path.isfile(self.fnidx):
            log.debug("read shapefile and create spatial index...")
            for obj in self.iterShapes():
                self.sidx.insert(obj.bbox)
            self.sidx.write(self.fnidx)
            log.debug("... done")
        else:
            log.debug("open spatial index...")
            self.sidx.read(self.fnidx)

    def intersection(self, x, y):
        """Intersection with a point.

        :param x:
        :param y:
        :return: list of record indexes that intersects with this point.
        """
        p = Point(x, y)

        # Use the spatal index to find objects that intersects with the bbox
        ids = self.sidx.intersection(x, y)

        # Use geographic information to find objects that intersects
        polys = [shape(self.shape(i).__geo_interface__) for i in ids]
        return [i for (i, poly) in zip(ids, polys) if poly.intersection(p)]
