from core.Helper import *


class TrackingHelper(Helper):
    """docstring for TrackingHelper"""

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

        res = self.httpInterface.send(req, array_data, subURL)

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

        res = self.httpInterface.send(req, array_data, subURL)

        return res
