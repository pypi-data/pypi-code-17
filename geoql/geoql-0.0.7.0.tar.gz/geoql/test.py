import geojson
from geoql2 import geoql
import geoleaflet

g = geoql.loads(open('../examples/example_extract.geojson').read(), encoding="latin-1")
z = geoql.loads(open('../examples/example_zips.geojson').read(), encoding="latin-1")

g = g.properties_null_remove()\
     .tags_parse_str_to_dict()\
     .keep_by_property({"highway": {"$in": ["residential", "secondary", "tertiary"]}})
g = g.keep_within_radius((42.3551, -71.0656), 0.75, 'miles')  # Within 0.75 of Boston Common.
g = g.keep_that_intersect(z)  # Only those entries found in a Boston ZIP Code regions.
g = g.node_edge_graph() 

open('leaflet.html', 'w').write(geoleaflet.html(g)) # Create visualization.
