##
##


#
# __init__.py for awips.dataaccess package
#
#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    12/10/12                      njensen       Initial Creation.
#    Feb 14, 2013    1614          bsteffen       refactor data access framework
#                                                 to use single request.
#    Apr 09, 2013    1871          njensen      Add doc strings
#    Jun 03, 2013    2023          dgilling     Add getAttributes to IData, add
#                                               getLatLonGrids() to IGridData.
#
#

__all__ = [

           ]

import abc
from six import with_metaclass
class IDataRequest(with_metaclass(abc.ABCMeta, object)):
    """
    An IDataRequest to be submitted to the DataAccessLayer to retrieve data.
    """

    @abc.abstractmethod
    def setDatatype(self, datatype):
        """
        Sets the datatype of the request.

        :param datatype: A string of the datatype, such as "grid", "radar", "gfe", "obs"
        """
        return

    @abc.abstractmethod
    def addIdentifier(self, key, value):
        """
        Adds an identifier to the request.  Identifiers are specific to the
        datatype being requested.

        :param key: the string key of the identifier
        :param value: the value of the identifier
        """
        return

    @abc.abstractmethod
    def setParameters(self, params):
        """
        Sets the parameters of data to request.

        :param params: a list of strings of parameters to request
        """
        return

    @abc.abstractmethod
    def setLevels(self, levels):
        """
        Sets the levels of data to request.  Not all datatypes support levels.

        :param levels: a list of strings of level abbreviations to request
        """
        return

    @abc.abstractmethod
    def setEnvelope(self, env):
        """
        Sets the envelope of the request.  If supported by the datatype factory,
        the data returned for the request will be constrained to only the data
        within the envelope.

        :param env: a shapely geometry
        """
        return

    @abc.abstractmethod
    def setLocationNames(self, locationNames):
        """
        Sets the location names of the request.

                locationNames: a list of strings of location names to request
        """
        return

    @abc.abstractmethod
    def getDatatype(self):
        """
        Gets the datatype of the request

        :returns: the datatype set on the request
        """
        return

    @abc.abstractmethod
    def getIdentifiers(self):
        """
        Gets the identifiers on the request

        :returns: a dictionary of the identifiers
        """
        return

    @abc.abstractmethod
    def getLevels(self):
        """
        Gets the levels on the request

        :returns: a list of strings of the levels
        """
        return

    @abc.abstractmethod
    def getLocationNames(self):
        """
        Gets the location names on the request

        :returns: a list of strings of the location names
        """
        return

    @abc.abstractmethod
    def getEnvelope(self):
        """
        Gets the envelope on the request

        :returns: a rectangular shapely geometry
        """
        return



class IData(with_metaclass(abc.ABCMeta, object)):
    """
    An IData representing data returned from the DataAccessLayer.
    """

    @abc.abstractmethod
    def getAttribute(self, key):
        """
        Gets an attribute of the data.

        :param key: the key of the attribute

        :returns: the value of the attribute
        """
        return

    @abc.abstractmethod
    def getAttributes(self):
        """
        Gets the valid attributes for the data.

        :returns: a list of strings of the attribute names
        """
        return

    @abc.abstractmethod
    def getDataTime(self):
        """
        Gets the data time of the data.

        :returns: the data time of the data, or None if no time is associated
        """
        return

    @abc.abstractmethod
    def getLevel(self):
        """
        Gets the level of the data.

        :returns: the level of the data, or None if no level is associated
        """
        return

    @abc.abstractmethod
    def getLocationName(self, param):
        """
        Gets the location name of the data.

        :returns: the location name of the data, or None if no location name is
                associated
        """
        return



class IGridData(IData):
    """
    An IData representing grid data that is returned by the DataAccessLayer.
    """

    @abc.abstractmethod
    def getParameter(self):
        """
        Gets the parameter of the data.

        :returns: the parameter of the data
        """
        return

    @abc.abstractmethod
    def getUnit(self):
        """
        Gets the unit of the data.

        :returns: the string abbreviation of the unit, or None if no unit is associated
        """
        return

    @abc.abstractmethod
    def getRawData(self):
        """
        Gets the grid data as a numpy array.

        :returns: a numpy array of the data
        """
        return

    @abc.abstractmethod
    def getLatLonCoords(self):
        """
        Gets the lat/lon coordinates of the grid data.

        :returns: a tuple where the first element is a numpy array of lons, and the
            second element is a numpy array of lats
        """
        return



class IGeometryData(IData):
    """
    An IData representing geometry data that is returned by the DataAccessLayer.
    """

    @abc.abstractmethod
    def getGeometry(self):
        """
        Gets the geometry of the data.

        :returns: a shapely geometry
        """
        return

    @abc.abstractmethod
    def getParameters(self):
        """Gets the parameters of the data.

        :returns: a list of strings of the parameter names
        """
        return

    @abc.abstractmethod
    def getString(self, param):
        """
        Gets the string value of the specified param.

        :param param: the string name of the param

        :returns: the string value of the param
        """
        return

    @abc.abstractmethod
    def getNumber(self, param):
        """
        Gets the number value of the specified param.

        :param param: the string name of the param

        :returns: the number value of the param
        """
        return

    @abc.abstractmethod
    def getUnit(self, param):
        """
        Gets the unit of the specified param.

        :param param: the string name of the param

        :returns: the string abbreviation of the unit of the param
        """
        return

    @abc.abstractmethod
    def getType(self, param):
        """
        Gets the type of the param.

        :param param: the string name of the param

        :returns: a string of the type of the parameter, such as
            "STRING", "INT", "LONG", "FLOAT", or "DOUBLE"
        """
        return

