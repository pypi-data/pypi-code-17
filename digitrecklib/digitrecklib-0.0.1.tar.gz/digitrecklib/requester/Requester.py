from digitrecklib.requester.IRequester import *

class Requester(IRequester):
    """docstring for Requester"""

    '''
     * Assign Devices and gets tracking ID.
     *
     * @param deviceList : list of devices to be assign for sharing location with each other.
     * @return mixed
    '''

    def createSessions(self, deviceList):
        subURL = "/v1/session/create"
        req = "session_create"

        array_data = {PARAM_DEVICE_IDS: deviceList}

        res = self.request(req, array_data, subURL)

        return res

    '''
     * Release a tracking session with the list of device {see trackingId}.
     *
     * @param trackingId : trackingId received from assignDevice call.
     * @return mixed
    '''

    def releaseSession(self, trackingId):

        subURL = "/v1/session/release"
        req = "session_release"

        array_data = {PARAM_TRACKING_ID: trackingId}

        res = self.request(req, array_data, subURL)

        return res
    
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

        res = self.request(req, array_data, subURL)

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

        res = self.request(req, array_data, subURL)

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

        res = self.request(req, array_data, subURL)

        return res
