from cairn_geographics.gis_object import CairnGisObject

class Location(CairnGisObject):
    lat = None
    lon = None

    def __init__(self, *args):
        super(Location, self).__init__()
        if args:
            self.lat = args[0]
            self.lon = args[1]

    def to_string(self):
        return "Location(lat={lat}, lon={lon})".format(
            lat=self.lat,
            lon=self.lon
        )


    def region(self, region_type):
        return self.from_sexpr(["containing_region", self, region_type], result_type='Region')

    def driving_distance(self, end_location):
        return self.from_sexpr(["driving_distance", self, end_location], result_type='Measure')

    def driving_time(self, end_location):
        return self.from_sexpr(["driving_time", self, end_location], result_type='Measure')

    def component_sexpr(self):
        return ("location", self.lat, self.lon)

    @classmethod
    def from_dict(cls, data):
        assert data['type'] == 'Location'
        location = cls(data['lat'], data['lon'])
        location.evaluated = True
        return location
