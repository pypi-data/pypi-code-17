"""ZWay Session"""

import requests


class ZWaySession(requests.Session):
    """Session for Z-Way Automation API"""

    def __init__(self, *args, **kwargs) -> None:
        self.zway_baseurl = kwargs.get('baseurl')
        del kwargs['baseurl']
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs):
        url = self.zway_baseurl + "/ZAutomation/api/v1" + url
        return super().request(method, url, **kwargs)
