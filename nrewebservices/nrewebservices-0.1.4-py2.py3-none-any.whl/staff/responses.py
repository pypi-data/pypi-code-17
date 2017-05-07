from nrewebservices.common import SoapResponseObject
from nrewebservices.common import make_boolean_mapper, make_simple_mapper

class StationBoard(SoapResponseObject):
    field_map = [
            ('location_name', make_simple_mapper('locationName')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoard, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


