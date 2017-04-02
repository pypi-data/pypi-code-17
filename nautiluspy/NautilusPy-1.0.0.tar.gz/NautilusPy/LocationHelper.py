from core.Helper import *


class LocationHelper(Helper):
    """docstring for LocationHelper"""

    '''
    * Gets Device Location
    * device session.
    *
    * @param string deviceId : Device ID for which location is required..
    * @return mixed
    '''

    def getLocation(self, deviceId):
        subURL = "/v1/device/location"
        req = "device_location"

        array_data = {PARAM_DEVICE_ID: deviceId}

        res = self.httpInterface.send(req, array_data, subURL)

        return res

    '''
    * Gets Path between start and end Date for Device ID.
     *
     * @param string deviceId : Device ID for which location is required.
     * @param string endDate : end date.
     * @param string startDate : start date.
     * @return mixed
    '''

    def getPath(self, deviceId, endDate, startDate):
        subURL = "/v1/device/path"
        req = "device_path"

        array_data = {PARAM_DEVICE_ID: deviceId, PARAM_END_DATE: endDate, PARAM_START_DATE: startDate}

        res = self.httpInterface.send(req, array_data, subURL)

        return res

    '''
    * Checks for nearby devices in the given {@see range} around {@see lat}, {@see lng}.
     *
     * @param integer count : number of devices needed in the {@see $range}.
     * @param string accessKey : accesskey for device group.
     * @param double lat : latitude of center of the area to be searched.
     * @param double lng : longitude of center of the area to be searched.
     * @param integer range : radius of area to be searched for devices.
     * @return mixed
    '''

    def getNearbyDevice(self, count, accessKey, lat, lng, rangeD):
        subURL = "/v1/device/nearby"
        req = "nearby_devices"

        array_data = {PARAM_COUNT: count, PARAM_ACCESSKEY: accessKey, PARAM_LAT: lat, PARAM_LNG: lng, PARAM_RANGE: rangeD}

        res = self.httpInterface.send(req, array_data, subURL)

        return res