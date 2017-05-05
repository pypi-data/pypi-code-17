'''
This module provides some extensions to matplotlib.

:references:

  * `Colormaps <http://matplotlib.org/examples/color/colormaps_reference.html>`_

:dependencies:

  * numpy
  * matplotlib

:copyright:

  | Tom de Geus
  | tom@geus.me
  | http://www.geus.me
'''

import matplotlib.pyplot as plt
import matplotlib        as mpl
import numpy             as np
import os,re,sys

# ==============================================================================

def cdf(data,mode='continuous',**kwargs):
  '''
Plot cumulative probability density.

:arguments:

  **data** (``<numpy.ndarray>``)
    Data for which the cumulative probability density is plotted.

:options:

  **mode** ([``'continuous'``] | ``'line'`` | ``'bar'``)
    Plot modes. If set to ``continuous`` the actual data is used. For the other
    cases the data is binned.

:linestyle:

  See ``gplot.plot``. Some examples:

  **linestyle** ([``'-'``] | ``'--'`` | ``'-.'`` | ``None``)
    Line-style

  **linewidth** (``<float>``)
    Line-width (e.g. ``1.0``).

  **marker** (``<str>``)
    Marker.

:barstyle:

  **facecolor** (``<str>``)
    Face color of the patch-objects.

  **edgecolor** (``<str>``)
    Edge color of the patch-objects.

  **linestyle** ([``'solid'``] | ``'dashed'`` | ``'dashdot'`` | ``'dotted'``)
    Line-style of the outline of the patch-objects.

  **linewidth** ([``1.0``] | ``<float>``)
    Line-width of the outline of the patch-objects.

:histogram:

  **density** ([``True``] | ``False``)
    If set to ``True`` the area under the curve is normalized to one.

  **bins** ([``10``] | ``<int>``)
    Number of bins.

  **range** (``<list>``) *optional*
    Lower and upper limit of the bins. If not provided, range is simply
    ``(data.min(),data.max())``. NB: values outside the range are ignored.

  **weights** (``<numpy.ndarray>``) *optional*
    Weights, of the same shape as ``data``.

.. seealso::

  * `matplotlib.patches.Rectangle
    <http://matplotlib.org/api/patches_api.html#matplotlib.patches.Rectangle>`_.
  '''

  # plot continuous
  # ---------------

  if mode in ['continuous','c']:

    return plt.plot(np.sort(data),np.linspace(0.0,1.0,len(data)),**kwargs)

  # plot in bins
  # ------------

  histogram            = {}
  histogram['density'] = kwargs.pop('density',True)
  for key in ['bins','range','weights']:
    if key in kwargs:
      histogram[key] = kwargs.pop(key)

  # calculate histogram
  data,bin_edges = np.histogram(data,**histogram)
  data           = np.cumsum(data)
  data          /= data[-1]
  bin_edges     += np.diff(bin_edges)[0]/2.

  # plot as curve
  if mode in ['line','lines','l']:
    return plt.plot(np.cumsum(np.diff(bin_edges))+bin_edges[0]-np.diff(bin_edges)[0]/2.,data,**kwargs)

  # plot as bars
  if mode in ['bars','bar','b']:
    for i,(x0,dx,dy) in enumerate(zip(bin_edges[:-1],bin_edges[1:]-bin_edges[:-1],data)):
      plt.gca().add_patch(mpl.patches.Rectangle((x0,0),dx,dy,**kwargs))

  return None

# ==============================================================================
