################################################################################
# PUT COMMENTS HERE
################################################################################
# Python Modules/Libraries
import time
import datetime
from sqlalchemy import extract

# Package Modules
import smarttap.DB_Module as DBMod


################################################################################
################################################################################
class AnalysisControl(object):
    """ Class responsible for analysis code & interaction with Analysis DB """
    def __init__(self):
        # Analysis DB Variables
        self.StopAnBrd = ''
        self.StopAnAli = ''
        self.AnlyBase = ''
        self.AnlyEngine = ''
        self.AnlyCur_session = ''

        # Main Data DB Variables
        self.Route = ''
        self.Stop = ''
        self.Trip = ''
        self.RouteStop = ''
        self.Users = ''
        self.MainBase = ''
        self.MainEngine = ''
        self.MainCur_session = ''

    ############################################################################
    # Analysis Database/ Database Session Establishment
    def check_session(self):
        """ Checks to ensure current session is active """
        if type(self.AnlyCur_session) is str:
            raise DBMod.SessionError()

    def new_analysis_db(self, db_direct_name):
        """ Manages DB creation for Analysis DB """
        (self.StopAnBrd, self.StopAnAli, self.AnlyBase,
         self.AnlyEngine) = DBMod.new_database_anly(db_direct_name)

    def new_analysis_session(self, db_direct_name):
        """ Manages DB session for Analysis DB """
        (self.StopAnBrd, self.StopAnAli, self.AnlyBase, self.AnlyEngine,
         self.AnlyCur_session) = DBMod.new_session_anly(db_direct_name)

    # Main Database Session Establishment
    def new_main_session(self, db_direct_name):
        """ Manages DB session creation for Main DB """
        (self.Route, self.Stop, self.Trip,
         self.RouteStop, self.Users, self.MainBase, self.MainEngine,
         self.MainCur_session) = DBMod.new_session_main(db_direct_name)

    ############################################################################
    # Database Input
    def input_stop_usage(self, brd_data, ali_data):
        """ Inputs boarding and alighting data from the trip_to_stop_detail
        function into the Analysis DB """
        # Input into DB
        bulk_brd = []
        for row in brd_data:
            data = brd_data[row]
            new_brd = {'stopID': int(row[0]), 'stopLat': float(data[24]),
                       'stopLong': float(data[25]), 'routeID': row[1],
                       'userType': str(row[2]), 'date': row[3],
                       'T0': data[0], 'T1': data[1], 'T2': data[2],
                       'T3': data[3], 'T4': data[4], 'T5': data[5],
                       'T6': data[6], 'T7': data[7], 'T8': data[8],
                       'T9': data[9], 'T10': data[10], 'T11': data[11],
                       'T12': data[12], 'T13': data[13], 'T14': data[14],
                       'T15': data[15], 'T16': data[16], 'T17': data[17],
                       'T18': data[18], 'T19': data[19], 'T20': data[20],
                       'T21': data[21], 'T22': data[22], 'T23': data[23]}
            bulk_brd.append(new_brd)
        self.AnlyEngine.execute(self.StopAnBrd.__table__.insert(), bulk_brd)

        bulk_ali = []
        for row in ali_data:
            key_data = row
            data = ali_data[row]
            new_ali = {'stopID': key_data[0], 'stopLat': data[24],
                       'stopLong': data[25], 'routeID': key_data[1],
                       'userType': key_data[2], 'date': key_data[3],
                       'T0': data[0], 'T1': data[1], 'T2': data[2],
                       'T3': data[3], 'T4': data[4], 'T5': data[5],
                       'T6': data[6], 'T7': data[7], 'T8': data[8],
                       'T9': data[9], 'T10': data[10], 'T11': data[11],
                       'T12': data[12], 'T13': data[13], 'T14': data[14],
                       'T15': data[15], 'T16': data[16], 'T17': data[17],
                       'T18': data[18], 'T19': data[19], 'T20': data[20],
                       'T21': data[21], 'T22': data[22], 'T23': data[23]}
            bulk_ali.append(new_ali)
        self.AnlyEngine.execute(self.StopAnAli.__table__.insert(), bulk_ali)

    ############################################################################
    # Stop Functions
    def stop_usage_summary(self, out_file):
        """" Process trip data into board and alight counts per stop
        :param out_file - Directory and name for output file """
        stops = {}
        for stopID, stopLat, stopLong, in self.MainCur_session.query(
                self.Stop.stopID, self.Stop.stopLat, self.Stop.stopLong).all():
            stops[stopID] = (stopLat, stopLong)

        stop_usage = {}
        for brdS, aliS in self.MainCur_session.\
            query(self.Trip.brdStop, self.Trip.aliStop).all():
            # Boarding Data
            if brdS in stop_usage:
                stop_usage[brdS][0] += 1
            else:
                stop_usage[brdS] = [1, 0, stops[brdS][0], stops[brdS][1]]

            # Alighting Data
            if aliS in stop_usage:
                stop_usage[aliS][1] += 1
            else:
                stop_usage[aliS] = [0, 1, stops[aliS][0], stops[aliS][1]]

        if len(out_file) > 0:
            fhand = open(out_file, 'w')
            fhand.write('stopID,brd_count,ali_count,lat,long\n')
            for stop in stop_usage:
                outtype = "{0},{1},{2},{3},{4}\n"
                fhand.write(outtype.format(str(stop), str(stop_usage[stop][0]),
                                           str(stop_usage[stop][1]),
                                           str(stop_usage[stop][2]),
                                           str(stop_usage[stop][3])))
            fhand.close()

    def stop_usage_detail(self):
        """ Process trip data into board and alight counts based on stopID,
        routeID, userType and date. Counts made per hour. """
        stops = {}
        for stopID, stopLat, stopLong, in self.MainCur_session.query(
                self.Stop.stopID, self.Stop.stopLat, self.Stop.stopLong).all():
            stops[stopID] = (stopLat, stopLong)

        users = {}
        for userID, userType in self.MainCur_session.query(
                self.Users.userID, self.Users.userType).all():
            users[userID] = userType

        brd_data = {}
        ali_data = {}
        for brdStop, brdTime, aliStop, aliTime, routeID, userID, in self.\
                MainCur_session.query(self.Trip.brdStop, self.Trip.brdTime,
                                      self.Trip.aliStop, self.Trip.aliTime,
                                      self.Trip.routeID, self.Trip.userID):
            user_type = users[userID]

            # Boarding Data
            date_brd = brdTime.date()
            hour_brd = brdTime.hour
            if (brdStop, routeID, user_type, date_brd) in brd_data:
                brd_data[(brdStop, routeID, user_type, date_brd)][hour_brd] += 1
            else:
                brd_data[(brdStop, routeID, user_type,
                          date_brd)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        stops[brdStop][0], stops[brdStop][1]]
                brd_data[(brdStop, routeID, user_type, date_brd)][hour_brd] += 1

            # Alighting Data
            date_ali = aliTime.date()
            hour_ali = aliTime.hour
            if (aliStop, routeID, user_type, date_ali) in ali_data:
                ali_data[(aliStop, routeID, user_type, date_ali)][hour_ali] += 1
            else:
                ali_data[(aliStop, routeID, user_type,
                          date_ali)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        stops[aliStop][0], stops[aliStop][1]]
                ali_data[(aliStop, routeID, user_type, date_ali)][hour_ali] += 1
        return brd_data, ali_data

    def origin_destination(self, out_file):
        """ DO NOT USE - OLD VERSION NOW REPLACED BY V2, HIGHLY INACCURATE
        Rapid OD-Matrix computation
        :param out_file - Output file directory and name """
        stops = {}
        for stop in self.MainCur_session.query(self.Stop):
            stops[stop.stopID] = 0

        od_matrix = {}
        for stop in self.MainCur_session.query(self.Stop):
            od_matrix[stop.stopID] = stops

        for trip in self.MainCur_session.query(self.Trip):
            brd_s = trip.brdStop
            ali_s = trip.aliStop
            od_matrix[brd_s][ali_s] += 1

        if len(out_file) > 0:
            fhand = open(out_file, 'w')
            for stop in od_matrix:
                fhand.write(str(stop)+','+str(od_matrix[stop])+'\n')
        return od_matrix

    def origin_destination_v2(self, out_file):
        """ Improved OD-Matrix computation algorithm
        :param out_file - Output file directory and name """
        start = time.time()
        od_matrix = {}
        for brdS, aliS in self.MainCur_session.\
                query(self.Trip.brdStop, self.Trip.aliStop).all():
            mat_key = '{0}_{1}'.format(brdS, aliS)
            if mat_key in od_matrix:        # Add to existing
                od_matrix[mat_key] += 1
            else:                           # Create new
                od_matrix[mat_key] = 1
        end1 = time.time()
        print('OD-Matrix Created', round(end1-start, 8))

        if len(out_file) > 0:
            fhand = open(out_file, 'w')
            num_stops = 0
            col_count = 0

            # File Column labels
            fhand.write(',')
            for stop_col, in self.MainCur_session.query(self.Stop.stopID).all():
                fhand.write(str(stop_col) + ',')
                num_stops += 1  # use of stopID run to count #stops
            fhand.write('\n')
            end2 = time.time()

            for stop_row, in self.MainCur_session.query(self.Stop.stopID):
                fhand.write(str(stop_row) + ',')
                for stop_col, in self.MainCur_session.query(self.Stop.stopID):
                    mat_key = '{0}_{1}'.format(stop_row, stop_col)
                    if col_count < num_stops - 1:
                        if mat_key in od_matrix:
                            fhand.write(str(od_matrix[mat_key]) + ',')
                        else:
                            fhand.write('0,')
                        col_count += 1
                    else:
                        if mat_key in od_matrix:
                            fhand.write(str(od_matrix[mat_key]) + '\n')
                        else:
                            fhand.write('0\n')
                        col_count = 0
            fhand.close()
            end3 = time.time()
            print('File Output', round(end3-end2, 8))

    ############################################################################
    # Journey Functions
    def journey_long(self, journey, jid):
        """ Code for processing data for journeys with >2 trips
        :param journey - List of trip data for journey
        :param jid - Journey ID """
        count = 0
        for trip in journey:
            if count == 0:
                data = [trip[0], jid, trip[1], trip[2], trip[3], trip[4], 0,
                        trip[4] - trip[4], trip[4] - trip[3]]
            elif count > 0:
                data[6] += 1
                data[7] += trip[3] - data[5]  # Transit time (Jry BrdN - AliN-1)
                data[3] = trip[2]
                data[5] = trip[4]
                data[8] = data[5] - data[4]  # Total trip time
            count += 1
        return data

    def journey_analysis(self, out_file, time_filt, user_filt):
        """ Journey reconstruction using 1 or more trip(s). Rapid
        reconstruction of trips using common journeyID field within data set.
        Additional filtering is possible for a limited time period (days) or
        specific userIDs through the population of the time_filt or user_filt
        attributes.

        All data from this function is output to a .txt file at the output
        filename location. The data is of the format:
            userID, journeyID, initial board stop, final alight stop,
            initial board time, final alight time, total transit time,
            net travel time

        :param out_file - Output file directory and name
        :param time_filt - 0 for no filtering, or a list of dates to filter
                           for (e.g. [8,9]). Assumes only 1 month processed.
        :param user_filt - 0 for no filtering, or a file location for a .txt
                           file containing all desired userIDs. This file
                           should be in a format of one userID per line.

        journey_analysis(str, int/list, int/str) """
        # User Data
        users = {}
        if user_filt != 0:
            fhand = open(user_filt)
            for line in fhand:
                user_id = str(line.strip())
                if len(user_id) == 20:
                    users[user_id] = 0

        # Data filter/gather/organisation
        jrny = {}
        trip_count = 0
        if time_filt == 0 and user_filt == 0:  # Standard all DB Jrny Analysis
            for trip in self.MainCur_session.query(self.Trip).order_by(
                    self.Trip.tripNum):
                if trip.journeyID not in jrny:
                    trip_count += 1
                    jrny[trip.journeyID] = [(trip.userID, trip.brdStop,
                                             trip.aliStop, trip.brdTime,
                                             trip.aliTime)]
                else:
                    trip_count += 1
                    jrny[trip.journeyID].append((trip.userID, trip.brdStop,
                                                 trip.aliStop, trip.brdTime,
                                                 trip.aliTime))
        elif time_filt != 0 and user_filt != 0:  # Jrny Analysis for time & user
            for trip in self.MainCur_session.query(self.Trip).filter(
                    extract('day', self.Trip.brdTime).in_(
                        time_filt)).order_by(self.Trip.tripNum):
                if trip.userID in users:
                    if trip.journeyID not in jrny:
                        trip_count += 1
                        jrny[trip.journeyID] = [(trip.userID, trip.brdStop,
                                                 trip.aliStop, trip.brdTime,
                                                 trip.aliTime)]
                    else:
                        trip_count += 1
                        jrny[trip.journeyID].append((trip.userID, trip.brdStop,
                                                     trip.aliStop, trip.brdTime,
                                                     trip.aliTime))
        elif time_filt == 0 and user_filt != 0:  # Jrny Analysis for specif users
            for trip in self.MainCur_session.query(self.Trip).order_by(
                    self.Trip.tripNum):
                if trip.userID in users:
                    if trip.journeyID not in jrny:
                        trip_count += 1
                        jrny[trip.journeyID] = [(trip.userID, trip.brdStop,
                                                 trip.aliStop, trip.brdTime,
                                                 trip.aliTime)]
                    else:
                        trip_count += 1
                    jrny[trip.journeyID].append((trip.userID, trip.brdStop,
                                                 trip.aliStop, trip.brdTime,
                                                 trip.aliTime))
        elif time_filt != 0 and user_filt == 0:  # Jrny Analysis for specif days
            for trip in self.MainCur_session.query(self.Trip). \
                    order_by(self.Trip.tripNum). \
                    filter(extract('day', self.Trip.brdtime). \
                                   in_(time.filt)):
                if trip.journeyID not in jrny:
                    trip_count += 1
                    jrny[trip.journeyID] = [(trip.userID, trip.brdStop,
                                             trip.aliStop, trip.brdTime,
                                             trip.aliTime)]
                else:
                    trip_count += 1
                    jrny[trip.journeyID].append((trip.userID, trip.brdStop,
                                                 trip.aliStop, trip.brdTime,
                                                 trip.aliTime))
        print('Total Trips:', trip_count)
        print('Total Journeys:', len(jrny))

        # Output preparation
        fhand = open(out_file, 'w')
        a1 = 'eis,jrnyID,brdStop,aliStop,brdTime,aliTime,'
        a2 = 'numTransit,TransitTime,netTrvTime\n'
        fhand.write(a1 + a2)
        out_form = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n"

        # Data distribution/management
        for jrnyID in jrny:
            cr_jrny = jrny[jrnyID]
            if len(cr_jrny) == 1:
                data = [cr_jrny[0][0], jrnyID, cr_jrny[0][1], cr_jrny[0][2],
                        cr_jrny[0][3], cr_jrny[0][4], 0,
                        cr_jrny[0][4] - cr_jrny[0][4],
                        cr_jrny[0][4] - cr_jrny[0][3]]
            elif len(cr_jrny) == 2:
                data = [cr_jrny[0][0], jrnyID, cr_jrny[0][1], cr_jrny[1][2],
                        cr_jrny[0][3], cr_jrny[1][4], 1,
                        cr_jrny[1][3] - cr_jrny[0][4],
                        cr_jrny[1][4] - cr_jrny[0][3]]
            elif len(cr_jrny) > 2:
                data = self.journey_long(cr_jrny, jrnyID)

            # Output
            fhand.write(out_form.format(data[0], data[1], data[2], data[3],
                                        data[4], data[5], data[6], data[7],
                                        data[8]))
        fhand.close()
        return trip_count, len(jrny)

    ############################################################################
    # Route Functions
    def route_usage_summary(self, out_file):
        """ Process trip data based on routes
        :param out_file - Directory and name for output file """
        rte_usage = {}
        for routeID, in self.MainCur_session.query(self.Trip.routeID).all():
            if routeID in rte_usage:
                rte_usage[routeID] += 1
            else:
                rte_usage[routeID] = 1
        if len(out_file) > 0:
            fhand = open(out_file, 'w')
            fhand.write('routeID,trip_count\n')
            out = '{0},{1}\n'
            for route in rte_usage:
                fhand.write(out.format(str(route), str(rte_usage[route])))
            fhand.close()

    def route_usage_detail(self, out_file):
        """ Route usage based on 1 hour time-steps """
        rte_use = {}
        for routeID, brdT, aliT in self.MainCur_session.query(
                self.Trip.routeID, self.Trip.brdTime, self.Trip.aliTime).all():
            brd_hour = brdT.hour
            ali_hour = aliT.hour
            if routeID in rte_use:
                rte_use[routeID][0][brd_hour] += 1
                rte_use[routeID][1][ali_hour] += 1
            else:
                rte_use[routeID] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                rte_use[routeID][0][brd_hour] += 1
                rte_use[routeID][1][ali_hour] += 1

        fhand = open(out_file, 'w')
        head = "routeID"
        out = "{0}"
        for x in range(1, 49, 1):
            out += ",{0}".format({x})
            if x < 25:
                head += ",{0}hrBrd".format(x-1)
            else:
                head += ",{0}hrAli".format(x-25)
        out += "\n"
        head += "\n"
        fhand.write(head)
        for rte in rte_use:
            fhand.write(out.format(rte, *rte_use[rte][0], *rte_use[rte][1]))
        fhand.close()

    ############################################################################
    ############################################################################
    # General
    def delete_relation(self, relation):
        """ Deletes all records from specified DB relation/table """
        self.AnlyCur_session.query(relation).delete()
        self.AnlyCur_session.commit()

    def close_session(self):
        """ Ends current DB session """
        self.AnlyCur_session.close()
