#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Controller for power strips as manufactered by ANEL Elektronik
(`https://anel-elektronik.de/`_).
"""
import logging
import pprint
import urlparse
import datetime
import re

import requests
PATTERN_TIME = r'^.*?, (?P<dt>\d{2}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})$'
RE_TIME = re.compile(PATTERN_TIME)

DT_FORMAT = '%d.%m.%y %H:%M:%S'

STATUS_KEYS = (
    "device", "hostname", "ip_addr", "ip_mask", "ip_gateway",
    "mac_addr", "port", "temperature", "device_type"
)

DEVICE_TYPE_MAP = {
    'H': 'Home',
    'P': 'Pro',
    'O': 'ONE',
    'a': 'ADV',
    'h': 'HUT',
    'i': 'IO'
}


def parse_relais_status(data):
    """
    Parse relais status information.

    :param data: raw data string
    :return: key/value dictionary with relais state information
    :rtype: dict

    >>> import os
    >>> EXAMPLES = os.path.join(os.path.dirname(__file__), '../contrib/example_data')
    >>> STRG = os.path.join(EXAMPLES, 'strg.cfg')
    >>> os.path.isfile(STRG)
    True
    >>> data = open(STRG, "rb").read()
    >>> pd = parse_relais_status(data)
    >>> len(pd.keys())
    10
    >>> sorted(pd.keys())
    ['device', 'device_type', 'hostname', 'ip_addr', 'ip_gateway', 'ip_mask', 'items', 'mac_addr', 'port', 'temperature']
    >>> pd['device']
    'NET-PWRCTRL_04.0'
    >>> pd['device_type']
    'Pro'
    >>> pd['hostname']
    'EOS'
    >>> pd['ip_addr']
    '192.168.0.26'
    >>> pd['ip_gateway']
    '192.168.0.253'
    >>> pd['ip_mask']
    '255.255.255.0'
    >>> pd['mac_addr']
    'de:ad:be:ef:00:00'
    >>> pd['port']
    '80'
    >>> pd['temperature']
    '29.9'
    """
    data_list = data.split(";")

    if data_list[58] != 'end':
        raise ValueError("Bad status data: IDX #58 is not 'end'!");

    lena_strip = {
        'items': []
    }

    for k in range(len(STATUS_KEYS)):
        key = STATUS_KEYS[k]
        lena_strip[key] = data_list[k].strip()

    for i in range(8):
        relais_data = {
            'name': data_list[10 + i],
            'status': data_list[20 + i],
            'disabled': data_list[30 + i],
            'info': data_list[40 + i],
            # Permutation aus T, K - T=Timer, K=Keepalife eingeschaltet
            'timer_or_keepalive': data_list[50 + i],
            'id': i,
        }
        lena_strip['items'].append(relais_data)

    try:
        lena_strip['device_type'] = DEVICE_TYPE_MAP[lena_strip['device_type']]
    except KeyError:
        pass
                     
    return lena_strip


def parse_device_information(data):
    """
    Parse device information.

    :param data: raw data string
    :return: key/value dictionary with relais state information
    :rtype: dict

    >>> import os
    >>> EXAMPLES = os.path.join(os.path.dirname(__file__), '../contrib/example_data')
    >>> DATEN = os.path.join(EXAMPLES, 'daten.cfg')
    >>> os.path.isfile(DATEN)
    True
    >>> data = open(DATEN, "rb").read()
    >>> pd = parse_device_information(data)
    >>> len(pd.keys())
    12
    >>> pd['name']
    'EOS'
    >>> pd['_time']
    'Di, 25.04.17 09:18:23'
    >>> pd['time']
    datetime.datetime(2017, 4, 25, 9, 18, 23)
    >>> pd['_boot']
    (14300, 110)
    >>> pd['boot']
    datetime.datetime(1999, 12, 5, 3, 2, 30)
    >>> pd['relais_change']
    8
    >>> pd['io_change']
    0
    >>> pd['log_change']
    5
    >>> pd['clock_status']
    '1'
    >>> pd['ver']
    '4.3'
    >>> pd['device_type']
    'Pro'
    """
    data_list = data.split(";")

    if data_list[11] != 'end':
        raise ValueError("Bad status data: IDX #11 is not 'end'!");

    lena_strip = {
        # Hostname
        "name": data_list[0].strip(),
        # Uhrzeit
        "_time": data_list[1],
        # Die Zahl wird erhöht wenn des Status der Relais sich ändert.
        "relais_change": data_list[2],
        # Für die ADV, IO, HUT Version.
        # Die Zahl wird erhöht wenn IO sich ändert.
        "io_change": data_list[3],
        # Die Zahl wird erhöht wenn Log sich ändert.
        "log_change": data_list[4],
        # 1 = SNTP Server - Uhr gefunden, Zeit ok;
        # 2 = SNTP Server - keine Uhr gefunden
        "clock_status": data_list[5],
        "login": data_list[6],
        "ver": data_list[7],
        "_boot": (int(data_list[8]), int(data_list[9])),
        # H = Home
        # P = Pro
        # O = ONE
        # a = ADV
        # h = HUT
        # i = IO
        "device_type": data_list[10]
    }

    time_matcher = RE_TIME.match(lena_strip['_time'])
    if time_matcher:
        lena_strip['time'] = datetime.datetime.strptime(
                                    time_matcher.groupdict()['dt'],
                                    DT_FORMAT)
    else:
        self.log.warning("Bad date/time: {!r}".format(lena_strip['_time']))
        lena_strip['time'] = datetime.datetime.fromtimestamp(0)

    boot_seconds = int(data_list[8])
    lena_strip['boot'] = lena_strip['time'] - datetime.timedelta(seconds=boot_seconds)

    for int_key in ("relais_change", "io_change", "log_change"):
        if lena_strip[int_key].strip() == '':
            value = 0
        else:
            value = int(lena_strip[int_key])
        lena_strip[int_key] = value

    try:
        lena_strip['device_type'] = DEVICE_TYPE_MAP[lena_strip['device_type']]
    except KeyError:
        pass

    return lena_strip


class LenaPowerstripRequestException(BaseException):
    pass


class LenaPowerstrip(object):
    """
    Controller for accessing power strips' web interface.
    May be used to toggle outlet on or off.
    """

    def __init__(self, *args, **kwargs):
        netloc = '{hostname}:{port}'.format(
            hostname=kwargs.get("hostname", "net-control"),
            port = kwargs.get("port", 80))
        self.auth = kwargs.get("auth")
        self._base_url = urlparse.urlunparse(
            (
                kwargs.get("scheme", 'http'),
                netloc,
                '', None, None, None
            )
        )
        self.log = logging.getLogger(__name__)
        self.args = kwargs.get("args")

    def relais(self, **kwargs):
        if kwargs.get("data"):
            r_status = kwargs.get("data")
        else:
            r_status = self.get_status(**kwargs)
        return [item['status'] == '1' for  item in r_status['items']]

    def __getitem__(self, relais_idx):
        relais_data = self.relais()
        return relais_data[relais_idx]

    def __setitem__(self, relais_idx, value):
        enable = value in (1, '1', True)
        relais_data = self.relais()

        if relais_data[relais_idx] == enable:
            # no change needed
            return

        # ... set value
        self.toggle_relais(relais=[relais_idx])
        relais_data_current = self.relais()
        if relais_data_current[relais_idx] == relais_data[relais_idx]:
            raise AssertionError("relais state was not altered!")

        if relais_data_current[relais_idx] != enable:
            raise AssertionError("relais state does not meet expectation!")

    def toggle_relais(self, **kwargs):
        """
        Toggle relais on or off.

        :param relais: list containing the IDs of outlets to be toggled
        :return:
        """
        params = dict()
        for relais_id in kwargs.get("relais"):
            key = 'F{:d}'.format(relais_id)
            params[key] = 'S'

        try:
            req = requests.post(
                urlparse.urljoin(self._base_url, "ctrl.htm"), auth=kwargs.get("auth", self.auth), data=params)
        except requests.exceptions.ConnectionError, rexc:
            self.log.error(rexc)
            raise LenaPowerstripRequestException("Connection Error")

        if req.status_code / 100 > 2:
            raise LenaPowerstripRequestException("Bad Response: {!r} {!s}".format(req.status_code, req.text))

    def get_status(self, **kwargs):
        """
        Retrieve outlets' status information.

        :param auth: credentials
        :return: dictionary with information about outlets and host
        :rtype: dict
        """
        req = requests.get(
            urlparse.urljoin(self._base_url, "strg.cfg"), auth=kwargs.get("auth", self.auth))

        try:
            lena_strip = parse_relais_status(req.text)
            self.log.debug(pprint.pformat(lena_strip))
        except ValueError, vexc:
            self.log.error(vexc)
            self.log.debug(req.text)
            raise
            
        return lena_strip

    def get_daten(self, **kwargs):
        """
        Retrieve basic device and software information.

        :param auth: credentials
        :return: key/value dictionary with device and software information
        :rtype: dict
        """
        try:
            req = requests.get(
                urlparse.urljoin(self._base_url, "daten.cfg"), auth=kwargs.get("auth", self.auth))
        except requests.exceptions.ConnectionError, rexc:
            self.log.error(rexc)
            raise LenaPowerstripRequestException("Connection Error")

        if req.status_code / 100 > 2:
            raise LenaPowerstripRequestException("Bad Response: {!r} {!s}".format(req.status_code, req.text))

        try:
            lena_strip = parse_device_information(req.text)
            self.log.debug(pprint.pformat(lena_strip))
        except ValueError, vexc:
            self.log.error(vexc)
            self.log.debug(req.text)
            raise

        return lena_strip

    def cli_device_status(self):
        device_information = self.get_daten()
        status_information = self.get_status()
        relais_information = self.relais(data=status_information)
        device_information.update(status_information)
        if self.args.privacy:
            privacy = dict(ip_addr="192.168.0.1", mac_addr="00:de:ad:be:ef:00")
            device_information.update(privacy)
        device_information['mac_addr'] = device_information['mac_addr'].lower()

        print "Host         : {hostname} ({mac_addr}) {ip_addr}".format(**device_information)
        print "Device       : {device} ({device_type}) v{ver}".format(**device_information)

        if self.args.verbose:
            print "Local time   : {time} -- \"{tainted}\"".format(time=device_information['time'].strftime("%Y-%m-%d %H:%M"),
                tainted=device_information['clock_status'] == '1' and "SNTP Server - Uhr gefunden, Zeit ok;" or "SNTP Server - keine Uhr gefunden")
            print "Temperature  : {temperature!s}".format(**device_information)

        if self.args.verbose == 0:
            print "Relais       : {:s}".format(' '.join([val and "ON " or "OFF" for val in relais_information]))
        else:
            for idx, val in enumerate(relais_information):
                print "Relais #{:d}    : {:s}".format(idx, val and "ON" or "OFF")

    def main(self):
        rc = None

        if not self.args:
            self.log.warning("No CLI args, no gain.")
            return 1

        if not len(self.args.actions):
            self.log.warning("You answered without saying anything. That's politics.")
            return 2

        for action in self.args.actions:
            try:
                func = getattr(self, 'cli_{:s}'.format(action))
                func()
            except AttributeError:
                self.log.error('%s', "Not implemented: {!r}?".format(action))
                rc = -2

        if rc is None:
            rc = 0

        return rc

if __name__ == '__main__':
    import doctest

    (FAILED, SUCCEEDED) = doctest.testmod()
    print "[doctest] SUCCEEDED/FAILED: %d/%d" % (SUCCEEDED, FAILED)
