# using dask for out of core processing on large rasters
# https://gist.github.com/lpinner/bd57b54a5c6903e4a6a2

import rasterio
from shapely.geometry import Point, LineString

def add_height_points(raster, points):
	"""
	Return the raster values at a given set of points.

	Parameters
	----------
	raster (rasterio) : a raster file opened with rasterio
	points (array of shapely Point)

	Returns
	-------
	result (array of shapely Point)

	"""
	# better way than making LineString just to get coords?
	pts = LineString(points)
	zs = src.sample(pts.coords, indexes=src.indexes)
	result = [Point(p[0],p[1],z) for p, z in zip(pts.coords, zs)]
	return result

def add_height_line(raster, line):
	"""
	Return the raster values at line vertices.

	Parameters
	----------
	raster (rasterio) : a raster file opened with rasterio
	line (shapely LineString)

	Returns
	-------
	result (shapely LineString)

	"""
	# have to drop any existing Z information at coord[2] or sample will fail
	pts = LineString([Point(coord[0],coord[1]) for coord in line.coords])
	# better way than making LineString just to get coords?
	zs = src.sample(pts.coords, indexes=src.indexes)
	result = [Point(p[0],p[1],z) for p, z in zip(pts.coords, zs)]
	return LineString(result)
