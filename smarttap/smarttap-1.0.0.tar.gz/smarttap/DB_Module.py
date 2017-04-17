################################################################################
# DBMS interface module for all package databases. Utilising SQLAlchemy package
# to communicate with the SQLite DBMS to store all data.
#
# This should be the only module requiring modification if a different DBMS
# is utilised. Further testing is however required.
################################################################################
# Python Modules/Libraries
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, String, Date, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


################################################################################
################################################################################
# Error Classes
class InvalidDBName(Exception):
    """ Error class to handle invalid DB name"""
    def __init__(self):
        pass


class SessionError(Exception):
    """ Error class to handle no active session for DB interaction"""
    def __init__(self):
        pass


################################################################################
################################################################################
# DATABASES
################################################################################
# Raw Database
def new_session_raw(db__direct_name):
    """ Creates new session for a Raw SQLite DB at given directory

    :param db__direct_name - Directory & DB name (str)

    new_session_raw(str) -> class (x4), SQLAlch Base, SQLAlch Engine,
    SQLAlch Session
    """
    ext_check = db__direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            engine_name = "sqlite:///{0}".format(db__direct_name)
            base = automap_base()
            engine = create_engine(engine_name)
            base.prepare(engine, reflect=True)

            rawtrip = base.classes.rawtrip
            extract_user = base.classes.extractuser
            extract_route = base.classes.extractroute
            extract_stop = base.classes.extractstop
            gtfs_stop = base.classes.gtfsstop
            gtfs_route = base.classes.gtfsroute

            session_new = sessionmaker(bind=engine)
            session = session_new()

            return rawtrip, extract_user, extract_route, extract_stop, \
                   gtfs_stop, gtfs_route, base, engine, session
        except Exception as e:
            print(e)
    else:
        return InvalidDBName()


def new_database_raw(db_direct_name):
    """ Creates new instance of Raw SQLite DB at given directory. Tables are
    designed for the 2015 TransLink GoCard data format, based upon the GTFS.

    :param db_direct_name - directory & DB name (str)

    new_database_raw(str) -> RawTrip, ExtractUser, ExtractRoute, ExtractStop
    """
    ext_check = db_direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            # Initialise SQLAlchemy ORM
            engine_name = "sqlite:///{0}".format(db_direct_name)
            engine = create_engine(engine_name)
            base = declarative_base()

            class RawTrip(base):
                """ Database class for raw Translink GoCard trip data

                Attr: operator, operations date, run, route, service,
                direction, scheduled start, actual start, actual end,
                vehicle, eis, boarding time, alighting time, ticket type,
                low zone, high zone, passengers, boarding stop, alighting stop,
                journey ID, trip ID
                """
                __tablename__ = 'rawtrip'
                rtID = Column(Integer, primary_key=True)
                optor = Column(String(30))
                ops_date = Column(String(23))
                route = Column(String(7))
                service = Column(String(7))
                run = Column(String(7))
                direct = Column(String(10))
                eis = Column(String(20))
                brd_time = Column(String(23))
                ali_time = Column(String(23))
                brd_stop = Column(String(6))
                ali_stop = Column(String(6))
                tick_typ = Column(String(60))
                jrny_id = Column(String(25))
                trip_id = Column(Integer)

            class ExtractUser(base):
                """ Database class for user info from GoCard data.

                userID: unique eis field value
                userType: extracted from first half of tick_typ
                """
                __tablename__ = 'extractuser'
                userID = Column(String(20), primary_key=True)
                userType = Column(String(20), nullable=False)

            class ExtractRoute(base):
                """ Database class for route info from GoCard data.

                routeID: unique route field value
                optor: associated optor field value
                """
                __tablename__ = 'extractroute'
                routeID = Column(String(4), primary_key=True)
                optor = Column(String(30), nullable=False)

            class ExtractStop(base):
                """ Database class for stop info from GoCard data.

                stopID: unique stop value from brd or ali stop fields
                """
                __tablename__ = 'extractstop'
                stopID = Column(String(10), primary_key=True)

            class GTFSStop(base):
                """ Database class for GTFS stop data."""
                __tablename__ = 'gtfsstop'
                stopID = Column(Integer, primary_key=True)
                stopCode = Column(String(10))
                stopName = Column(String(100))
                stopLat = Column(Float)
                stopLong = Column(Float)
                stopZone = Column(Integer)
                locType = Column(Integer)
                parStat = Column(String(20))
                platCode = Column(String(5))

            class GTFSRoute(base):
                """ Database class for GTFS route data."""
                __tablename__ = 'gtfsroute'
                routeID = Column(String(4), primary_key=True)
                routeName = Column(String(100))
                routeType = Column(Integer)

            base.metadata.create_all(engine)

            return RawTrip, ExtractUser, ExtractRoute, ExtractStop, GTFSStop,\
                   GTFSRoute, base, engine
        except Exception as e:
            print('Error:', e)
    else:
        raise InvalidDBName()


################################################################################
# Main Database
def new_session_main(db_direct_name):
    """ Creates new session for a Main SQLite DB at given directory

    :param db__direct_name - Directory & DB name (str)

    new_session_main(str) -> class (x4), SQLAlch Base, SQLAlch Engine,
    SQLAlch Session
    """
    ext_check = db_direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            engine_name = "sqlite:///{0}".format(db_direct_name)
            base = automap_base()
            engine = create_engine(engine_name)
            base.prepare(engine, reflect=True)

            route = base.classes.route
            stop = base.classes.stop
            tripdata = base.classes.tripdata
            routestop = base.classes.routestop
            user = base.classes.users

            session_new = sessionmaker(bind=engine)
            session = session_new()

            return route, stop, tripdata, routestop, user, base, engine, session
        except Exception as e:
            print(e)
    else:
        return InvalidDBName()


def new_database_main(db_direct_name):
    """ Creates new instance of Main SQLite DB at given directory. Tables are
    designed for the 2015 TransLink GoCard data format, based upon the GTFS.

    :param db_direct_name - directory & DB name (str)

    new_database_main(str) -> Route, Stop, TripData, RouteStop, Users
    """
    ext_check = db_direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            #Initialise SQLAlchemy ORM
            engine_name = "sqlite:///{0}".format(db_direct_name)
            engine = create_engine(engine_name)
            base = declarative_base()

            class Route(base):
                """ Route data class for organisation of route info

                routeID: Translink GTFS route code (e.g. '139', 'NHAM')
                routeName: Translink GTFS route name (e.g. 'Spring Hill Loop')
                routeType: Translink GTDS route type (0 = Light Rail, 2 = Train,
                                                      3 = Bus, 4 = Ferry)
                operator: Route operator (e.g. 'Brisbane Transport')
                """
                __tablename__ = 'route'
                routeID = Column(String(4), primary_key=True)
                routeName = Column(String(100))
                routeType = Column(Integer, nullable=False)
                operator = Column(String(30), nullable=False)

            class Stop(base):
                """ Stop data class for organisation of stop info

                stopID: Translink GTFS stop code (e.g. '1799', 'C86', '10823')
                stopName: GTFS specified stop name (e.g. 'Sandgate Rd, stop 3')
                stopZone: Zone in Translink network (e.g. 1, 23, 5)
                stopLat: Latitude of stop (e.g. -27.33)
                stopLong: Longitude of stop (e.g. 153.04)
                """
                __tablename__ = 'stop'
                stopID = Column(Integer, primary_key=True)
                stopName = Column(String(250))
                stopZone = Column(Float)
                stopLat = Column(Float, nullable=False)
                stopLong = Column(Float, nullable=False)

            class Users(base):
                """ Class to store information on system users

                userID: GoCard data unique ID for each user
                userType: Card type (Child, Senior, Adult, Student)
                """
                __tablename__ = 'users'
                userID = Column(String(20), primary_key=True)
                userType = Column(String(20), nullable=False)

            class TripData(base):
                """ Trip data class for organisation of user trips

                routeID: References routeID in Route class
                serviceID: Translink GTFS service number for a given route
                run: Route-Service run number
                userID: GoCard data unique ID for each user
                direction: either inbound or outbound
                brdTime: date-time stamp for boarding onto transport service
                aliTime: date-time stamp for alighting from transport service
                brdStop: stop at which service was boarded
                aliStop: stop at which service was alighted
                journeyID: GoCard data unique ID for each journey (trip group)
                tripNum: number of trip in a specific journey
                """
                __tablename__ = 'tripdata'
                routeID = Column(String(4), ForeignKey('route.routeID'))
                serviceID = Column(String(7))
                run = Column(String(7))
                userID = Column(String(20), ForeignKey('users.userID'))
                tripDirect = Column(String(8), nullable=False)
                brdTime = Column(DateTime(timezone=False), nullable=False)
                aliTime = Column(DateTime(timezone=False), nullable=False)
                brdStop = Column(Integer, ForeignKey('stop.stopID'))
                aliStop = Column(Integer, ForeignKey('stop.stopID'))
                journeyID = Column(String(25))
                tripNum = Column(Integer)

                __table_args__ = (PrimaryKeyConstraint('routeID', 'userID',
                                                       'brdTime'), {},)

                route = relationship(Route, foreign_keys=[routeID])
                users = relationship(Users, foreign_keys=[userID])
                stop_brd = relationship(Stop, foreign_keys=[brdStop])
                stop_ali = relationship(Stop, foreign_keys=[aliStop])

            class RouteStop(base):
                """ Route stop pairs (In/Out) info

                routeID: References routeID in Route class
                id: Integer ID for stop pair in overall route (Origin UQ)
                inStop: Inbound stopID
                outStop: Outbound stopID
                avgLat: Average latitude of inbound and outbound stops
                avgLong: Average longitude of inbound and outbound stops
                """
                __tablename__ = 'routestop'
                routeID = Column(String(4), ForeignKey('route.routeID'))
                pairID = Column(Integer)
                inStop = Column(Integer, ForeignKey('stop.stopID'))
                outStop = Column(Integer, ForeignKey('stop.stopID'))
                avgLat = Column(Float, nullable=False)
                avgLong = Column(Float, nullable=False)

                __table_args__ = (PrimaryKeyConstraint('routeID', 'pairID'),
                                  {},)

                route = relationship(Route, foreign_keys=[routeID])
                stop_in = relationship(Stop, foreign_keys=[inStop])
                stop_out = relationship(Stop, foreign_keys=[outStop])

            base.metadata.create_all(engine)

            return Route, Stop, TripData, RouteStop, Users, base, engine
        except Exception as e:
            print(e)
    else:
        raise InvalidDBName()


################################################################################
# Analysis Database
def new_session_anly(db_direct_name):
    """ Creates new session for an Analysis SQLite DB at given directory.

    :param db__direct_name - Directory & DB name (str)

    new_session_anly(str) -> class (x2), SQLAlch Base, SQLAlch Engine,
    SQLAlch Session
    """
    ext_check = db_direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            engine_name = "sqlite:///{0}".format(db_direct_name)
            base = automap_base()
            engine = create_engine(engine_name)
            base.prepare(engine, reflect=True)

            stop_analysis_brd = base.classes.stopanbrd
            stop_analysis_ali = base.classes.stopanali

            session_new = sessionmaker(bind=engine)
            session = session_new()

            return stop_analysis_brd, stop_analysis_ali, base, engine, session
        except Exception as e:
            print(e)
    else:
        return InvalidDBName()


def new_database_anly(db_direct_name):
    """ Creates new instance of Analysis SQLite DB at given directory. Tables
    are designed to accommodate data from the Stop_Analysis function

    :param db_direct_name: directory & DB name (str)

    new_database_anly(str) -> StopAnBrd, StopAnAli
    """
    ext_check = db_direct_name.split('.')
    if ext_check[1] == 'db':
        try:
            engine_name = "sqlite:///{0}".format(db_direct_name)
            engine = create_engine(engine_name)
            base = declarative_base()

            class StopAnBrd(base):
                """ Stop_Analysis data class for output boarding stop data.

                stopID: Translink GTFS stop code (e.g. 1799, 900086, 10823)
                stopLat: Latitude of stop (e.g. -27.3345)
                stopLong: Longitude of stop (e.g. 153.0434)
                routeID: Translink GTFS route code (e.g. '139', 'NHAM')
                userType: Go Card type (Child, Senior, Adult, Student)
                date: Date of the data. datetime.date() format (e.g. 21/08/2015)
                T0-T23: Counts for each hour (0000hrs - 2300hrs)
                """
                __tablename__ = 'stopanbrd'
                stopID = Column(Integer)
                stopLat = Column(Float)
                stopLong = Column(Float)
                routeID = Column(String(4))
                userType = Column(String(20))
                date = Column(Date)
                T0 = Column(Integer)
                T1 = Column(Integer)
                T2 = Column(Integer)
                T3 = Column(Integer)
                T4 = Column(Integer)
                T5 = Column(Integer)
                T6 = Column(Integer)
                T7 = Column(Integer)
                T8 = Column(Integer)
                T9 = Column(Integer)
                T10 = Column(Integer)
                T11 = Column(Integer)
                T12 = Column(Integer)
                T13 = Column(Integer)
                T14 = Column(Integer)
                T15 = Column(Integer)
                T16 = Column(Integer)
                T17 = Column(Integer)
                T18 = Column(Integer)
                T19 = Column(Integer)
                T20 = Column(Integer)
                T21 = Column(Integer)
                T22 = Column(Integer)
                T23 = Column(Integer)

                __table_args__ = (PrimaryKeyConstraint('stopID', 'routeID',
                                                       'userType', 'date'), {},)

            class StopAnAli(base):
                """ Stop_Analysis data class for organising the output of
                analysis on alighting stop data.

                stopID: Translink GTFS stop code (e.g. 1799, 900086, 10823)
                stopLat: Latitude of stop (e.g. -27.3345)
                stopLong: Longitude of stop (e.g. 153.0434)
                routeID: Translink GTFS route code (e.g. '139', 'NHAM')
                userType: Go Card type (Child, Senior, Adult, Student)
                date: Date of the data. datetime.date() format (e.g. 21/08/2015)
                T0-T23: Counts for each hour (0000hrs - 2300hrs)
                """
                __tablename__ = 'stopanali'
                stopID = Column(Integer)
                stopLat = Column(Float)
                stopLong = Column(Float)
                routeID = Column(String(4))
                userType = Column(String(20))
                date = Column(Date)
                T0 = Column(Integer)
                T1 = Column(Integer)
                T2 = Column(Integer)
                T3 = Column(Integer)
                T4 = Column(Integer)
                T5 = Column(Integer)
                T6 = Column(Integer)
                T7 = Column(Integer)
                T8 = Column(Integer)
                T9 = Column(Integer)
                T10 = Column(Integer)
                T11 = Column(Integer)
                T12 = Column(Integer)
                T13 = Column(Integer)
                T14 = Column(Integer)
                T15 = Column(Integer)
                T16 = Column(Integer)
                T17 = Column(Integer)
                T18 = Column(Integer)
                T19 = Column(Integer)
                T20 = Column(Integer)
                T21 = Column(Integer)
                T22 = Column(Integer)
                T23 = Column(Integer)

                __table_args__ = (PrimaryKeyConstraint('stopID', 'routeID',
                                                       'userType', 'date'), {},)

            base.metadata.create_all(engine)

            return StopAnBrd, StopAnAli, base, engine
        except Exception as e:
            print(e)
    else:
        raise InvalidDBName()
