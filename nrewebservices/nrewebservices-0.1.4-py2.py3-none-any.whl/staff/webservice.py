from .responses import StationBoard

from suds.client import Client
from suds.sax.element import Element

import datetime
import logging
import pytz

log = logging.getLogger(__name__)
TOKEN_NAMESPACE = ('com','http://thalesgroup.com/RTTI/2013-11-28/Token/types')

class Session(object):
    """
    This class provides an interface to the LDBWS Staff Version web service session.
    """
    def __init__(self, wsdl=None, api_key=None, timeout=5):

        # Try getting the WSDL and API KEY from the environment if they aren't explicitly passed.
        if not wsdl:
            try:
                wsdl = os.environ['NRE_STAFF_WSDL']
            except AttributeError:
                raise ValueError("LDBWS Staff Version WSDL must be either explicitly provided to the Session initializer or via the environment variable NRE_STAFF_WSDL.")

        if not api_key:
            try:
                api_key = os.environ['NRE_STAFF_API_KEY']
            except AttributeError:
                raise ValueError("LDBWS Staff Version API key must be either explicitly provided to the Session initializer or via the environment variable NRE_STAFF_API_KEY.")

        # Build the SOAP client.
        self._soap_client = Client(wsdl)
        self._soap_client.set_options(timeout=timeout)
        self._service = self._soap_client.service['LDBSVServiceSoap']
        self._reference_service = self._soap_client.service['LDBSVRefServiceSoap']

        # Build the SOAP authentication headers.
        access_token = Element('AccessToken', ns=TOKEN_NAMESPACE)
        access_token_value = Element('TokenValue', ns=TOKEN_NAMESPACE)
        access_token_value.setText(api_key)
        access_token.append(access_token_value)
        self._soap_client.set_options(soapheaders=(access_token))

    def get_station_board_by_crs(self, crs, rows=10, include_departures=True, include_arrivals=False,
            from_filter_crs=None, to_filter_crs=None, time=None, time_window=None):

        # Get the appropriate SOAP query method.
        if include_departures and include_arrivals:
            query = self._service.GetArrivalDepartureBoardByCRS
        elif include_departures:
            query = self._service.GetDepartureBoardByCRS
        elif include_arrivals:
            query = self._service.GetArrivalBoardByCRS
        else:
            raise ValueError("When calling get_station_board_by_crs, either include_departures or include_arrivals must be set to True.")

        # Construct the query parameters.
        params = {}
        params['crs'] = crs
        params['numRows'] = rows
        if to_filter_crs:
            if from_filter_crs:
                log.warn("get_station_board_by_crs() can only be filtered on one of from_filter_crs and to_filter_crs. Since both are provided, using only to_filter_crs")
            params['filterCrs'] = to_filter_crs
            params['filterType'] = 'to'
        elif from_filter_crs:
            params['filterCrs'] = from_filter_crs
            params['filterType'] = 'from'
        if time is not None:
            params['time'] = time
        else:
            params['time'] = datetime.datetime.now(pytz.timezone("Europe/London"))
        if time_window is not None:
            params['timeWindow'] = time_window
        else:
            params['timeWindow'] = 120

        # Do the SOAP query.
        # TODO: Some form of error handling.
        soap_response = query(**params)
        return StationBoard(soap_response)


