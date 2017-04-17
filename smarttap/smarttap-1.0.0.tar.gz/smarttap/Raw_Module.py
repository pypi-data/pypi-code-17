################################################################################
# Module for pre-processing of raw GoCard & GTFS data sets for input into the
# main SmartTAP DB. Functions include input, processing/analysis & output of
# these. Additional functions provided after the RawDataControl class to
# split files for testing, and check for duplicates in GTFS data sets.
################################################################################
# Python Modules/Libraries
import time

# Package Modules/Libraries
import smarttap.DB_Module as DBMod


################################################################################
################################################################################
# Raw Data Module Class
class RawDataControl(object):
    """ Class for input, processing, analysis and output of raw GoCard and
    GTFS data prior to use in main DB. Functions grouped based on role."""
    def __init__(self):
        self.RawTrip = ''
        self.ExtractUser = ''
        self.ExtractRoute = ''
        self.ExtractStop = ''
        self.GTFSStop = ''
        self.GTFSRoute = ''
        self.Base = ''
        self.engine = ''
        self.cur_session = ''

    ############################################################################
    # Database/Session Establishment
    def check_session(self):
        """ Checks if a session is active, raising an error if it is not"""
        if type(self.cur_session) is str:
            raise DBMod.SessionError()

    def new_raw_database(self, db_direct_name):
        """ Database creation for RawDataControl class
        :param db_direct_name: directory & DB name (str)
        """
        (self.RawTrip, self.ExtractUser, self.ExtractRoute, self.ExtractStop,
         self.GTFSStop, self.GTFSRoute, self.Base,
         self.engine) = DBMod.new_database_raw(db_direct_name)

    def new_raw_session(self, db_direct_name):
        """ Database session creation for RawDataControl class
        :param db_direct_name: directory & DB name (str)
        """
        (self.RawTrip, self.ExtractUser, self.ExtractRoute, self.ExtractStop,
         self.GTFSStop, self.GTFSRoute, self.Base, self.engine,
         self.cur_session) = DBMod.new_session_raw(db_direct_name)

    ############################################################################
    ############################################################################
    # DATA INPUT
    ############################################################################
    # Raw Trips
    def new_rawtrip_file_core(self, filename):
        """ Imports multiple trips from .txt file using SQL Alchemy Core
        :param filename: Input file directory /name.txt

        new_rawtrip_file_core(str) -> tot_count(int)
        """
        tot_count = 0
        bulk_trips = []
        try:
            fhand = open(filename, 'r')
            for line in fhand:
                tot_count += 1
                trip = line.split(',')
                (optor, ops_date, route, service, run, direct, eis,
                 brd_time, ali_time, tick_typ, jrny_id,
                 trip_id) = (trip[0], trip[1], trip[3], trip[4], trip[2],
                             trip[5], trip[10], trip[11], trip[12], trip[13],
                             trip[19], trip[20])

                if trip[17].find('C') >= 0:
                    code = trip[17].split('C')
                    if len(code) == 2:
                        brd_stop = str(900000 + int(code[1]))
                    else:
                        brd_stop = trip[17]
                elif trip[17].find('A') >= 0:
                    code = trip[17].split('A')
                    if len(code) == 2:
                        brd_stop = 31
                    else:
                        brd_stop = trip[17]
                else:
                    brd_stop = trip[17]

                if trip[18].find('C') >= 0:
                    code = trip[18].split('C')
                    if len(code) == 2:
                        ali_stop = str(900000 + int(code[1]))
                    else:
                        ali_stop = trip[18]
                elif trip[18].find('A') >= 0:
                    code = trip[18].split('A')
                    if len(code) == 2:
                        ali_stop = 31
                    else:
                        ali_stop = trip[18]
                else:
                    ali_stop = trip[18]

                if optor == 'Queensland Rail' and route == 'Unknown':
                    route = 'RAIL'

                new_trip = {'rtID': tot_count, 'optor': optor,
                            'ops_date': ops_date, 'route': route,
                            'service': service, 'run': run, 'direct': direct,
                            'eis': eis, 'brd_time': brd_time,
                            'ali_time': ali_time,  'brd_stop': brd_stop,
                            'ali_stop': ali_stop, 'tick_typ': tick_typ,
                            'jrny_id': jrny_id, 'trip_id': trip_id}
                bulk_trips.append(new_trip)
            fhand.close()
            self.engine.execute(self.RawTrip.__table__.insert(), bulk_trips)
            return tot_count
        except Exception as e:
            print(tot_count, e)

    def get_rawtrip(self):
        """ Returns current raw trips in DB """
        out_trip = []
        for trip in self.cur_session.query(self.RawTrip).all():
            out_trip.append([trip.route, trip.eis, trip.brd_time])
        return out_trip

    ############################################################################
    # GTFS Stop
    def new_gtfsstop_file_core(self, filename):
        """ Imports GTFS stop data from .txt files using SQL Alchemy Core.
        :param filename: Input file directory /name.txt

        new_gtfsstop_file_core(str) -> tot_count(int)
        """
        tot_count = 0
        bulk_stops = []
        try:
            fhand = open(filename, 'r')
            for line in fhand:
                tot_count += 1
                stop1 = line.split(',"')
                stop11 = stop1[0].split(',')
                stop2 = stop1[1].split('",')
                stop21 = stop2[1].split(',')

                (stopID, stopCode, stopName, stopLat, stopLon, locType,
                 parStat, platCode) = (int(stop11[0]), stop11[1], stop2[0],
                                       float(stop21[1]), float(stop21[2]),
                                       int(stop21[5]), stop21[6], stop21[7])
                if stop21[3].find('/') > 0:
                    zns = stop21[3].split('/')
                    stopZone = (int(zns[0]) + int(zns[1]))/2
                elif stop21[3].find('.') > 0:
                    stopZone = float(stop21[3])
                else:
                    stopZone = int(stop21[3])

                new_stop = {'stopID': stopID, 'stopCode': stopCode,
                            'stopName': stopName, 'stopLat': stopLat,
                            'stopLong': stopLon, 'stopZone': stopZone,
                            'locType': locType, 'parStat': parStat,
                            'platCode': platCode}
                bulk_stops.append(new_stop)
            fhand.close()
            self.engine.execute(self.GTFSStop.__table__.insert(), bulk_stops)
            return tot_count
        except Exception as e:
            print(tot_count, e)

    def get_gtfsstop(self):
        """ Returns current GTFS stops in DB """
        out_stop = []
        for stop in self.cur_session.query(self.GTFSStop).all():
            out_stop.append([stop.stopID, stop.stopName])
        return out_stop

    ############################################################################
    # GTFS Route
    def new_gtfsroute_file_core(self, filename):
        """ Imports GTFS route data from .txt files using SQL Alchemy Core.
        :param filename: Input file directory /name.txt

        new_gtfsroute_file_core(str) -> tot_count(int)
        """
        fhand = open(filename, 'r')
        tot_count = 0
        bulk_routes = []
        try:

            for line in fhand:
                tot_count += 1
                route1 = line.split(',"')
                route11 = route1[0].split(',')
                route2 = route1[1].split('",')
                route21 = route2[1].split(',')

                (routeID, routeName, routeType) = (str(route11[1]), str(route2[0]),
                                                   route21[1])

                new_route = {'routeID': routeID, 'routeName': routeName,
                         'routeType': routeType}
                bulk_routes.append(new_route)
            fhand.close()
            self.engine.execute(self.GTFSRoute.__table__.insert(), bulk_routes)
            return tot_count
        except Exception as e:
            print('Error:', e)

    def get_gtfsroutes(self):
        """ Returns current GTFS routes in DB """
        out_route = []
        for route in self.cur_session.query(self.GTFSRoute).all():
            out_route.append([route.routeID, route.routeName])
        return out_route

    ############################################################################
    # Extract User
    def get_extruser(self):
        """ Returns users in raw GoCard data """
        out_user = []
        for user in self.cur_session.query(self.ExtractUser).all():
            out_user.append((user.userID, user.userType))
        return out_user

    ############################################################################
    # Extract Route
    def get_extrroute(self):
        """ Returns routes in raw GoCard data """
        out_route = []
        for route in self.cur_session.query(self.ExtractRoute).all():
            out_route.append((route.routeID, route.operator))
        return out_route

    ############################################################################
    # Extract Stop
    def get_extrstop(self):
        """ Returns stops in raw GoCard data """
        out_stop = []
        for stop in self.cur_session.query(self.ExtractStop).all():
            out_stop.append(stop.stopID)
        return out_stop

    ############################################################################
    # General
    def delete_relation(self, relation):
        """ Deletes all records from specified DB relation/table """
        self.cur_session.query(relation).delete()
        self.cur_session.commit()

    def close_session(self):
        """ Ends current DB session """
        self.cur_session.close()

    ############################################################################
    ############################################################################
    # Data Extraction
    def user_extract(self):
        """ Extracts unique GoCard data userIDs and associated card types """
        # DB Querying/Extraction
        users = {}
        start1 = time.time()
        for user, cardT in self.cur_session.query(self.RawTrip.eis,
                                                  self.RawTrip.tick_typ):
            type1 = cardT.split('[')
            if user not in users:
                users[user] = type1[0].strip()
        end1 = time.time()

        # DB Input
        bulk_users = []
        start2 = time.time()
        for user in users:
            new_user = {'userID': user, 'userType': users[user]}
            bulk_users.append(new_user)
        self.engine.execute(self.ExtractUser.__table__.insert(), bulk_users)
        end2 = time.time()

        # Final output
        return end1 - start1, end2 - start2

    def route_extract(self):
        """ Extracts unique GoCard data routes and associated operators """
        # DB Querying/Extraction
        routes = {}
        start1 = time.time()
        for route, optor in self.cur_session.query(self.RawTrip.route,
                                                   self.RawTrip.optor):
            if route not in routes:
                routes[route] = optor
        end1 = time.time()

        # DB Input
        bulk_routes = []
        start2 = time.time()
        for route in routes:
            new_route = {'routeID': route, 'optor': routes[route]}
            bulk_routes.append(new_route)
        self.engine.execute(self.ExtractRoute.__table__.insert(), bulk_routes)
        end2 = time.time()

        # Final output
        return end1 - start1, end2 - start2

    def stop_extract(self):
        """ Extracts unique GoCard data brd & ali stop IDs """
        # DB Querying/Extraction
        stops = []
        start1 = time.time()
        for brdS, aliS in self.cur_session.query(self.RawTrip.brd_stop,
                                                 self.RawTrip.ali_stop):
            if brdS not in stops:
                stops.append(brdS)
            if aliS not in stops:
                stops.append(aliS)
        end1 = time.time()

        # DB Input
        bulk_stops = []
        start2 = time.time()
        for stop in stops:
            bulk_stops.append({'stopID': stop})
        self.engine.execute(self.ExtractStop.__table__.insert(), bulk_stops)
        end2 = time.time()

        return end1 - start1, end2 - start2

    def extract_all(self):
        uT1, uT2 = self.user_extract()
        rT1, rT2 = self.route_extract()
        sT1, sT2 = self.stop_extract()
        return uT1, uT2, rT1, rT2, sT1, sT2

    ############################################################################
    ############################################################################
    # Data Output
    def trip_output(self, filename):
        """ Outputs trip data in format for input into Main SQLite DB

        :param filename: File output location/name for trip data set
        """
        fhand = open(filename, 'w')
        out_form = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'
        for trip in self.cur_session.query(self.RawTrip).\
                order_by(self.RawTrip.eis):
            fhand.write(out_form.format(trip.route, trip.service, trip.run,
                                        trip.eis, trip.direct, trip.brd_time,
                                        trip.ali_time, trip.brd_stop,
                                        trip.ali_stop, trip.jrny_id,
                                        trip.trip_id))
        fhand.close()

    def user_output(self, filename):
        """ Outputs user data in format for input into Main SQLite DB

        :param filename: File output location/name for user data set
        """
        fhand = open(filename, 'w')
        out_form = '{0},{1}\n'
        for user in self.cur_session.query(self.ExtractUser):
            fhand.write(out_form.format(user.userID, user.userType))
        fhand.close()

    def route_output(self, filename):
        """ Outputs route data in format for input into Main SQLite DB.
        Information extracted from the raw trip data and GTFS route data sets
        are used to output the required information.

        :param filename: File output location/name for route data set
        """
        fhand = open(filename, 'w')
        out_form = '{0};{1};{2};{3}\n'
        gtfs = {}
        for route in self.cur_session.query(self.GTFSRoute):
            gtfs[route.routeID] = (route.routeName, route.routeType)
        for route, optor in self.cur_session.query(self.ExtractRoute.routeID,
                                                   self.ExtractRoute.optor):
            if route in gtfs:
                fhand.write(out_form.format(route, gtfs[route][0],
                                            gtfs[route][1], optor))
        fhand.close()

    def stop_output(self, filename):
        """ Outputs stop data in format for input into Main SQLite DB.
        Information extracted from the raw trip data and GTFS stop data sets
        are used to output the required information.

        :param filename: File output location/name for stop data set
        """
        fhand = open(filename, 'w')
        out_form = '{0};{1};{2};{3};{4}\n'
        gtfs = {}
        for stop in self.cur_session.query(self.GTFSStop):
            gtfs[stop.stopID] = (stop.stopName, stop.stopZone,
                                 stop.stopLat, stop.stopLong)
        for stop, in self.cur_session.query(self.ExtractStop.stopID):
            try:
                if stop == '':
                    pass
                if stop.startswith('DH'):
                    pass
                elif int(stop) in gtfs:
                    stp = int(stop)
                    fhand.write(out_form.format(stp, gtfs[stp][0], gtfs[stp][1],
                                                gtfs[stp][2], gtfs[stp][3]))
            except ValueError:
                pass
        fhand.close()

    ############################################################################
    ############################################################################
    # Data Analysis
    def stop_compare(self):
        """ Compares stop in GoCard data with stops in GTFS data """
        # Gather data sets
        gc_stops = []
        for stop, in self.cur_session.query(self.ExtractStop.stopID):
            gc_stops.append(stop)
        gtfs_stops = set()
        for stop, in self.cur_session.query(self.GTFSStop.stopID):
            gtfs_stops.add(str(stop))

        # Comparison
        error = []
        for stop in gc_stops:
            if stop not in gtfs_stops:
                error.append(stop)
        return error

    def route_compare(self):
        """ Compares routes in GoCard data with routes in GTFS data """
        # Gather data sets
        gc_routes = []
        for route in self.cur_session.query(self.ExtractRoute.routeID):
            gc_routes.append(route)
        gtfs_routes = set()
        for route in self.cur_session.query(self.GTFSRoute.routeID):
            gtfs_routes.add(route)

        # Comparison
        error = []
        for route in gc_routes:
            if route not in gtfs_routes:
                error.append(route)
        return error

    def stop_tripCount(self, inFile, outFile):
        """ Generates brd & ali counts for stops listed in file inFile """
        stops = {}
        fhand = open(inFile, 'r')
        for line in fhand:
            stops[line.strip()] = 0
        for brdS, aliS in self.cur_session.query(self.RawTrip.brd_stop,
                                                 self.RawTrip.ali_stop):
            if brdS in stops:
                stops[brdS] += 1
            if aliS in stops:
                stops[aliS] += 1

        fhand.close()
        fhand = open(outFile, 'w')
        for stop in stops:
            fhand.write('{0},{1}\n'.format(stop, stops[stop]))


def dup_finder(filename, unique_attr):
    """ Function to find duplicates in GTFS stop or route files

    :param filename: Input file location
    :param unique_attr: Attribute row in data set to be checked for duplicates

    dup_finder(str, int) -> str
    """
    fhand = open(filename, 'r')
    uid = {}
    for line in fhand:
        line1 = line.split(',"')
        line2 = line1[0].split(',')

        if line2[unique_attr] not in uid:
            uid[line2[unique_attr]] = 1
        else:
            uid[line2[unique_attr]] += 1
    fhand.close()
    for unique in uid:
        if uid[unique] > 1:
            print(unique)


def card_type_finder(filename):
    """ Function to extract all unique values from a data set

    :param filename: input filename fro analysis

    card_type_finder(str) -> list
    """
    fhand = open(filename, 'r')
    types = {}
    for line in fhand:
        line1 = line.split(',')
        line2 = line1[13].split('[')
        type_u = line2[0].strip()
        if type_u not in types:
            types[type_u] = 1
        else:
            types[type_u] += 1
    fhand.close()
    print(types)


def file_split_user(filename, file_direct, file_users):
    """ Function to split large raw trip data sets based on userIDs

    :param filename - file location for input data
    :param file_direct - main directory for all files to be saved to
    :param file_users - number of users to have trips in each file

    file_split_user(str, str, int) -> None
    """
    count = 1
    user_id = {}
    fhand_in = open(filename, 'r')
    fhand_out = open(file_direct+str(count)+'.txt', 'w')
    for line in fhand_in:
        a = line.split(',')
        if a[3] not in user_id:
            user_id[a[3]] = 0

        if len(user_id) <= file_users:
            fhand_out.write(line)
        elif len(user_id) > file_users:
            fhand_out.close()
            user_id = {}
            count += 1
            fhand_out = open(file_direct+str(count)+'.txt', 'w')
            user_id[a[3]] = 0
            fhand_out.write(line)
    fhand_out.close()
    fhand_in.close()


def file_split_date(filename, file_direct, mth_yr):
    """ Function to split large raw trip data sets based on date in brdTime.
    This function assumes that data is only supplied for a period within a
    single month.

    Input:
    :param filename - file location for input data
    :param file_direct - main directory for all files to be saved to
    :param mth_yr - str for month & year of data

    file_split_date(str, str, str) -> None
    """
    fhand_in = open(filename, 'r')

    # Calculating the dates in the data set & assigning trips to each date
    dates = {}
    filter_days = {}
    error_count = 0
    for line in fhand_in:
        a = line.split(',')
        if a[5][:10] == '1899-12-30' or a[6][:10] == '1899-12-30':
            date = 0
        else:
            date = a[5][8:10]  # BrdT

        if date == 0:
            error_count += 1
        elif date not in dates:
            dates[date] = 1
            filter_days[date] = [line]
        else:
            dates[date] += 1
            filter_days[date].append(line)
    fhand_in.close()
    day_count = sorted(dates.items())
    print('Trip Counts per Day:', day_count)

    for day in filter_days:
        fhand_out = open(file_direct + 'rTrip_' + day + mth_yr + '.txt', 'w')
        for line in filter_days[day]:
            fhand_out.write(line)
        fhand_out.close()

    return error_count, day_count
