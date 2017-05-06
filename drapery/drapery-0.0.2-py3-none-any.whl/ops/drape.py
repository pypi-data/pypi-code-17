import .sample
from shapely.geometry import Point, LineString

def drape(raster, feature, return_points=False):
	"""
	Convert a 2D feature to a 3D feature by sampling a raster

	Parameters
	----------
	raster (rasterio) - raster to provide the z coordinate
	feature (dict) - fiona feature record to convert

	Returns
	-------
	result (Point or Linestring) - shapely Point or LineString of xyz coordinate triples
	
	"""
	coords = feature['geometry']['coordinates']
	geom_type = feature['geometry']['type']

	if geom_type == 'Point':
		xyz = sample(raster, [coords])
		result = Point(xyz[0])
	elif geom_type == 'LineString':
		xyz = sample(raster, coords)
		points = [Point(x,y,z) for x,y,z in xyz]
		result = LineString(points)
	else:
		logging.error('drape not implemented for {}'.format(geom))

	return result
