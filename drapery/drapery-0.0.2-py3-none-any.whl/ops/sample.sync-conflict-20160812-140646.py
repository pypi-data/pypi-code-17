# using dask for out of core processing on large rasters
# https://gist.github.com/lpinner/bd57b54a5c6903e4a6a2
import logging
import rasterio
from shapely.geometry import shape, Point, LineString

def sample(raster, coords):
	"""
	Return a 3D LineString with the z coordinates sampled from an input raster

	Parameters
	----------
	raster (rasterio)
	coords - array of tuples containing coordinate pairs (x,y) or triples (x,y,z)

	Returns
	-------
	result - array of tuples containing coordinate triples (x,y,z)
	"""
	if len(coords[0]) == 3:
		logging.info('Input is a 3D geometry. Z coordinates will be updated.')
		z = raster.sample([(x,y) for x,y,z in coords], indexes=raster.indexes)
	else:
		z = raster.sample(coords, indexes=raster.indexes)

	result = [(vert[0],vert[1],vert_z) for vert, vert_z in zip(coords, z)]

	return result

def add_height_points(raster, features):
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
	with rasterio.open(raster) as src:
		points = [shape(point['geometry']) for point in features]
		pts = LineString(points)
		zs = src.sample(pts.coords, indexes=src.indexes)
		result = [Point(p[0],p[1],z) for p, z in zip(pts.coords, zs)]
	return result

def add_height_line(raster, features):
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
	with rasterio.open(raster) as src:
		pts = [shape(line['geometry']) for line in features]
		# better way than making LineString just to get coords?
		zs = src.sample(pts.coords, indexes=src.indexes)
		result = [Point(p[0],p[1],z) for p, z in zip(pts.coords, zs)]
	return LineString(result)
