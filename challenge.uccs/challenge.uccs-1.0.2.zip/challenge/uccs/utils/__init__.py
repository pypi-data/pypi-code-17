from .read_data import *

import bob.ip.facedetect

def bounding_box(bbx):
  """Converts a bounding box (x, y, w, h) into a :py:class:`bob.ip.facedetect.BoundingBox`"""
  return bob.ip.facedetect.BoundingBox((bbx[1], bbx[0]), size = (bbx[3], bbx[2]))

def overlap(gt, det):
  """Computes the overlap between two :py:class:`bob.ip.facedetect.BoundingBox`'es using a variant of the Jaccard index (intersection over union).

  As the ground-truth is usually larger than the face, we do not punish bounding boxes that are smaller than the ground truth.
  Therefore, the union (the denominator) takes into account only one fourth of the ground truth boudning box -- or the intersection area, whichever is larger:

  .. math::
     O(G,D) = \\frac{|G \\cap D|}{|G \\tilde{\\cup} D|} = \\frac{G \\cap D}{\\max\{\\frac{|G|}4, |G \\cap D|\} + |D| - |G \\cap D|}

  where :math:`|\\dot|` is the area operator.
  Hence, when the detected bounding box :math:`D` covers at least a fourth of the ground-truth bounding box :math:`G` and is entirely contained inside :math:`G`, an overlap of 1 is reached.
  """

  intersection = gt.overlap(det)

  # negative size of intersection: no intersection
  if any(s <= 0 for s in intersection.size_f):
    # no overlap
    return 0.

  # compute union; reduce required overlap to the ground truth
  union = max(gt.area/4, intersection.area) + det.area - intersection.area

  # return intersection over modified union (modified Jaccard similarity)
  return intersection.area / union


def split_data_list_into_parallel(data, processes, arguments):
  """Splits a ``list`` of elements into the given number of parallel lists of lists, so that they can be used by ``multiprocessing``.

  The arguments is a possible ``tuple`` of additional arguments passed to the parallel function."""
  return [([d for i, d in enumerate(data) if i % processes == p], ) + arguments for p in range(processes)]

def split_data_dict_into_parallel(data, processes, arguments):
  """Splits a ``dict`` of elements into the given number of parallel lists of dictionaries, so that they can be used by ``multiprocessing``.

  The arguments is a possible ``tuple`` of additional arguments passed to the parallel function."""
  return [({f:v for i,(f,v) in enumerate(data.items()) if i % processes == p}, ) + arguments for p in range(processes)]
