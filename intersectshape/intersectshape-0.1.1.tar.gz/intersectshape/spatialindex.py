#!/usr/bin/env python3.6
# coding: utf-8


"""Simple spatial index."""


import logging
import numpy


# Log
log = logging.getLogger('intersectshape.spatialindex')


class SpatialIndex(object):
    """Spatial index."""

    def __init__(self):
        self.bboxs = list()

    def insert(self, bbox):
        """Add bounding box.

        :param bbox: (xmin, ymin, xmax, ymax)
        """
        self.bboxs.append(bbox)

    def write(self, fn):
        """Write index file.

        :param fn: path of filename.
        """
        if fn.endswith('.npy'):
            fn = fn[:-4]
        numpy.save(fn, self.bboxs)
        log.debug(f"write spatial index to '{fn}.npy' ok")

    def read(self, fn):
        """Read index file.

        :param fn: path of filename.
        """
        if not fn.endswith('.npy'):
            fn += '.npy'
        self.bboxs = numpy.load(fn)
        log.debug(f"read spatial index from '{fn}' ok")

    def intersection(self, x, y):
        """Get rectangle id that intersects a point.

        :param x: x's coordinate of a point.
        :param y: y's coordinate of a point.
        :return: list of ids.
        """
        log.debug(f"spatialindex: compute intersection with point "
                  f"({x}, {y}) ...")
        if type(self.bboxs) is not numpy.ndarray:
            self.bboxs = numpy.array(self.bboxs)

        # Check bounds
        logic = numpy.empty_like(self.bboxs)
        logic[:, 0] = (x >= self.bboxs[:, 0])
        logic[:, 2] = (x <= self.bboxs[:, 2])
        logic[:, 1] = (y >= self.bboxs[:, 1])
        logic[:, 3] = (y <= self.bboxs[:, 3])

        # Get indices of point inside rectangles
        iids = numpy.argwhere(logic.all(axis=1)).flatten().tolist()
        log.debug(f"spatialindex: intersection done: found {iids}")
        return iids
