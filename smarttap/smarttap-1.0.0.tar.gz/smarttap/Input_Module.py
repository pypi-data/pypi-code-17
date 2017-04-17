################################################################################
# PUT COMMENTS HERE
################################################################################
# Python Modules/Libraries
import time
import datetime as dt

# Package Modules
import smarttap.DB_Module as DBMod


################################################################################
# Error Classes
class DataError(Exception):
    def __init__(self):
        pass


class ForeignKeyError(Exception):
    def __init__(self, route):
        self.route=route

    def __repr__(self):
        return self.route


################################################################################
# Input Module
class InputControl(object):
    """ Class responsible for primary database & input"""
    def __init__(self):
        self.Route = ''
        self.Stop = ''
        self.TripData = ''
        self.RouteStop = ''
        self.Users = ''
        self.Base = ''
        self.engine = ''
        self.cur_session = ''

    ############################################################################
    # Error checking
    def check_session(self):
        """ Checks current session is active """
        if type(self.cur_session) is str:
            raise DBMod.SessionError()
    
    ############################################################################
    # DB/Session Establishment
    def new_main_database(self, db_direct_name):
        """ Manages DB creation for Main DB"""
        (self.Route, self.Stop, self.TripData, self.RouteStop, self.Users,
         self.Base, self.engine) = DBMod.new_database_main(db_direct_name)

    def new_main_session(self, db_direct_name):
        """ Manages DB session creation for Main DB"""
        (self.Route, self.Stop, self.TripData,
         self.RouteStop, self.Users, self.Base, self.engine,
         self.cur_session) = DBMod.new_session_main(db_direct_name)

    ############################################################################
    ############################################################################
    # DATA QUERY FUNCTIONS
    ############################################################################
    # Route Functions
    def new_route_file_core(self, filename):
        """ Import route data from .txt or .csv file into Main DB
        :param filename - filename with directory (str)

        new_route_file_core(str) -> int, int, int """
        fhand = open(filename, 'r')
        err_count = 0
        tot_count = 0
        bulk_routes = []
        route_id = []
        cur_routes = self.get_routes()
        try:
            for line in fhand:
                tot_count += 1
                # Split/Prepare data from raw input
                route = line.split(';')
                route[0].strip()
                route[1].strip()
                route[2].strip()
                route[2] = int(route[2])
                route[3].strip()

                # Check data accuracy
                if str(route[0]) in cur_routes:  # current routes
                    err_count += 1
                    pass
                elif str(route[0]) in route_id:  # current input
                    err_count += 1
                    pass
                elif len(route[0]) > 4:  # input length
                    err_count += 1
                    pass
                elif type(route[1]) is not str:  # type check
                    err_count += 1
                    pass
                elif route[2] not in [0, 2, 3, 4]:
                    err_count += 1
                    pass
                elif type(route[3]) is not str:  # type check
                    err_count += 1
                    pass
                else:
                    new_route = {'routeID': route[0], 'routeName': route[1],
                                 'routeType': route[2], 'operator': route[3]}
                    bulk_routes.append(new_route)
                    route_id.append(route[0])
            self.engine.execute(self.Route.__table__.insert(), bulk_routes)
            percent_error = (err_count / tot_count) * 100
            return err_count, tot_count, round(percent_error, 2)
        except DataError as e:
            print(tot_count)
            print('Error:', e)
        finally:
            fhand.close()  # Ensure handle closed

    def get_routes(self):
        """ Returns all route data in Main DB """
        out_route = {}
        for route in self.cur_session.query(self.Route):
            out_route[route.routeID] = 0
        return out_route

    ############################################################################
    # Stop Functions
    def new_stop_file_core(self, filename):
        """ Import stop data from .txt or .csv file into Main DB
        :param filename - filename with directory (str)

        new_stop_file_core(str) -> int, int, int """
        fhand = open(filename, 'r')
        err_count = 0
        tot_count = 0
        bulk_stops = []
        cur_stops = self.get_stops()
        try:
            for line in fhand:
                tot_count += 1
                # Split/Prepare data from raw input
                stop = line.split(';')
                stop[0].strip()
                stop[0] = int(stop[0])
                stop[1].strip()
                stop[2].strip()
                stop[2] = float(stop[2])
                stop[3].strip()
                stop[3] = float(stop[3])
                stop[4].strip()
                stop[4] = float(stop[4])

                # Check data accuracy
                if str(stop[0]) in cur_stops:  # current routes
                    err_count += 1
                    pass
                elif type(stop[0]) is not int:  # type check
                    err_count += 1
                    pass
                elif type(stop[1]) is not str:  # type check
                    err_count += 1
                    pass
                elif type(stop[2]) is not float:  # type check
                    err_count += 1
                    pass
                elif type(stop[3]) is not float:  # type check
                    err_count += 1
                    pass
                elif type(stop[4]) is not float:  # type check
                    err_count += 1
                    pass
                else:
                    new_stop = {'stopID': stop[0], 'stopName': stop[1],
                                'stopZone': stop[2], 'stopLat': stop[3],
                                'stopLong': stop[4]}
                    bulk_stops.append(new_stop)
            self.engine.execute(self.Stop.__table__.insert(), bulk_stops)
            percent_error = (err_count / tot_count) * 100
            return err_count, tot_count, round(percent_error, 2)
        except DataError as e:
            print('Error:', e)
        finally:
            fhand.close()  # ensure handle closed

    def get_stops(self):
        """ Returns all stop data in Main DB """
        out_stop = {}
        for stop in self.cur_session.query(self.Stop):
            out_stop[stop.stopID] = (stop.stopLat, stop.stopLong)
        return out_stop

    ############################################################################
    # RouteStop Functions
    def new_rtestp_file_core(self, filename):
        """ Import route-stop data from .txt or .csv file into Main DB
        :param filename - filename with directory (str)

        new_rtestp_file_core(str) -> int, int, int """
        fhand = open(filename, 'r')
        err_count = 0
        tot_count = 0
        bulk_rtestp = []
        cur_stops = self.get_stops()
        cur_routes = self.get_routes()
        cur_rtestps = self.get_rtestps()
        try:
            for line in fhand:
                tot_count += 1
                # Split/Prepare data from raw input
                rtestp = line.split(',')
                rtestp[0] = str(rtestp[0].strip())
                rtestp[1] = int(rtestp[1].strip())
                rtestp[2] = int(rtestp[2].strip())
                rtestp[3] = int(rtestp[3].strip())
                rtestp[4] = float(rtestp[4].strip())
                rtestp[5] = float(rtestp[5].strip())

                # Check data accuracy
                if rtestp[0] not in cur_routes:
                    err_count += 1
                    pass
                elif rtestp[2] not in cur_stops or rtestp[3] not in cur_stops:
                    err_count += 1
                    pass
                elif (rtestp[0], rtestp[1]) in cur_rtestps:
                    err_count += 1
                    pass
                else:
                    new_rtestp = {'routeID': rtestp[0], 'pairID': rtestp[1],
                                  'inStop': rtestp[2], 'outStop': rtestp[3],
                                  'avgLat': rtestp[4], 'avgLong': rtestp[5]}
                    bulk_rtestp.append(new_rtestp)
            self.engine.execute(self.RouteStop.__table__.insert(), bulk_rtestp)
            percent_error = (err_count / tot_count) * 100
            return err_count, tot_count, round(percent_error, 2)
        except DataError as e:
            print('Error:', e)
        finally:
            fhand.close()

    def get_rtestps(self):
        """ Returns all route-stop data in Main DB """
        out_rtestp = []
        for rtestp in self.cur_session.query(self.Route):
            out_rtestp.append((rtestp.routeID, rtestp.pairID))
        return rtestp

    ############################################################################
    # User Functions
    def new_user_file_core(self, filename):
        """ Import user data from .txt or .csv file into Main DB
        :param filename - filename with directory (str)

        new_user_file_core(str) -> int, int, int """
        fhand = open(filename, 'r')
        err_count = 0
        tot_count = 0
        bulk_users = []
        cur_users = self.get_users()
        try:
            for line in fhand:
                tot_count += 1
                # Split/Prepare data from raw input
                user = line.split(',')
                user[0] = str(user[0].strip())
                user[1] = str(user[1].strip())

                # Check data accuracy
                if user[0] in cur_users:
                    err_count += 1
                    pass
                elif len(user[0]) != 20:
                    err_count += 1
                    pass
                elif len(user[1]) > 20:
                    err_count += 1
                    pass
                else:
                    new_user = {'userID': user[0], 'userType': user[1]}
                    bulk_users.append(new_user)
            self.engine.execute(self.Users.__table__.insert(), bulk_users)
            percent_error = (err_count / tot_count) * 100
            return err_count, tot_count, round(percent_error, 2)
        except DataError as e:
            print('Error', e)
        finally:
            fhand.close()

    def get_users(self):
        """ Returns all user data in Main DB """
        out_user = {}
        for user in self.cur_session.query(self.Users):
            out_user[user.userID] = 0
        return out_user

    ############################################################################
    # TripData Functions
    def new_trip_file_core(self, filename, out_file):
        """ Import trip data from .txt or .csv file into Main DB
        :param filename - filename with directory (str)
        :param out_file - erroneous trip output file location

        new_trip_file_core(str, str) -> int, int, int, dict """
        fhand = open(filename, 'r')
        fhand_er = open(out_file, 'w')
        error_count = 0
        error_dict = {'Value Error': 0, 'Existing Trip': 0,
                      'Current Input': 0, 'Route not in DB': 0,
                      'Invalid ServiceID': 0, 'Invalid RunID': 0,
                      'User not in DB': 0, 'Alight before Board': 0,
                      '>24hr Trip': 0, 'Stop not in DB': 0,
                      'Invalid JourneyID': 0, 'Invalid TripID': 0}
        total_count = 0
        bulk_trips = []
        new_trips = {}
        dt_format = '%Y-%m-%d %H:%M:%S.%f'
        cur_stops = self.get_stops()
        cur_routes = self.get_routes()
        cur_users = self.get_users()
        cur_trips = self.get_trips()
        for line in fhand:
            total_count += 1
            # Reset data from previous loop
            rid = ''
            sv_id = ''
            run = ''
            user_id = ''
            direct = ''
            brd_t = ''
            ali_t = ''
            brd_s = 0
            ali_s = 0
            jrny_id = ''
            trip_id = 0

            # Split/Prepare data from raw input
            try:
                trip = line.split(',')
                rid = str(trip[0].strip())
                sv_id = str(trip[1].strip())
                run = str(trip[2].strip())
                user_id = str(trip[3].strip())
                direct = str(trip[4].strip())
                brd_t = dt.datetime.strptime(str(trip[5]), dt_format)
                ali_t = dt.datetime.strptime(str(trip[6]), dt_format)
                brd_s = int(trip[7].strip())
                ali_s = int(trip[8].strip())
                jrny_id = str(trip[9].strip())
                trip_id = int(trip[10].strip())
            except ValueError:
                error_count += 1
                error_dict['Value Error'] += 1
                fhand_er.write(line)
                pass

            # Check data accuracy
            if (rid, user_id, brd_t) in cur_trips:
                error_count += 1
                error_dict['Existing Trip'] += 1
                fhand_er.write(line)
                pass
            elif (rid, user_id, brd_t) in new_trips:
                error_count += 1
                error_dict['Current Input'] += 1
                fhand_er.write(line)
                pass
            elif rid not in cur_routes:
                error_count += 1
                error_dict['Route not in DB'] += 1
                fhand_er.write(line)
                pass
            elif len(sv_id) > 8:
                error_count += 1
                error_dict['Invalid ServiceID'] += 1
                fhand_er.write(line)
                pass
            elif len(run) > 8:
                error_count += 1
                error_dict['Invalid RunID'] += 1
                fhand_er.write(line)
                pass
            elif user_id not in cur_users:
                error_count += 1
                error_dict['User not in DB'] += 1
                fhand_er.write(line)
                pass
            # elif brd_t == '' or ali_t == '':
            #    error_count += 1
            #    pass
            elif brd_t > ali_t:
                error_count += 1
                error_dict['Alight before Board'] += 1
                fhand_er.write(line)
                pass
            elif ali_t - brd_t > dt.timedelta(days=1):
                error_count += 1
                error_dict['>24hr Trip'] += 1
                fhand_er.write(line)
                pass
            elif brd_s not in cur_stops or ali_s not in cur_stops:
                error_count += 1
                error_dict['Stop not in DB'] += 1
                fhand_er.write(line)
                pass
            elif len(jrny_id) != 25:
                error_count += 1
                error_dict['Invalid JourneyID'] += 1
                fhand_er.write(line)
                pass
            elif trip_id == 0:
                error_count += 1
                error_dict['Invalid TripID'] += 1
                fhand_er.write(line)
                pass
            else:
                new_trips[(rid, user_id, brd_t)] = 0
                new_trip = {'routeID': rid, 'serviceID': sv_id, 'run': run,
                            'userID': user_id, 'tripDirect': direct,
                            'brdTime': brd_t, 'aliTime': ali_t,
                            'brdStop': brd_s,
                            'aliStop': ali_s, 'journeyID': jrny_id,
                            'tripNum': trip_id}
                bulk_trips.append(new_trip)
        self.engine.execute(self.TripData.__table__.insert(), bulk_trips)
        fhand.close()  # ensure handle closed
        fhand_er.close()

        # Output
        # print(error_dict)
        percent_error = (error_count / total_count) * 100
        return error_count, total_count, round(percent_error, 2), error_dict

    def get_trips(self):
        """ Returns all trip data in Main DB"""
        out_trip = {}
        for trip in self.cur_session.query(self.TripData):
            out_trip[(trip.routeID, trip.userID, trip.brdTime)] = 0
        return out_trip

    ############################################################################
    # General
    def delete_relation(self, relation):
        """ Deletes all records from specified DB relation/table """
        self.cur_session.query(relation).delete()
        self.cur_session.commit()
