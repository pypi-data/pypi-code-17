################################################################################
# MODIFY INPUT NAMES FOR GTFS STOP & ROUTE FILES AS REQUIRED. CURRENTLY SET AS
# Stops_Raw.txt & Routes_Raw.txt, SEE LINES 55 & 56 TO CHANGE, RESPECTIVELY.
################################################################################
# Python Modules/Libraries
import time

# Package Modules
import smarttap.Raw_Module as RawMod
import smarttap.Input_Module as InpMod
import smarttap.Analysis_Module as AnlyMod


################################################################################
class RawDataManagement(object):
    """ Class to handle Raw Data Module in SmartTAP """
    def __init__(self, direct, db_name):
        """ Initialise RawDataManagement class
        :param direct - file location for data input & output
        :param db_name - database root name"""
        self.direct = direct
        self.db_name = db_name
        self.hand = RawMod.RawDataControl()

    def raw_database(self):
        """ Creation of new Raw SQLite DB & deletion of existing data """
        strt = time.time()
        # DB/Session Establishment
        self.hand.new_raw_database(self.direct+'Raw'+self.db_name)
        self.hand.new_raw_session(self.direct+'Raw'+self.db_name)

        # Delete Old Data
        self.hand.delete_relation(self.hand.RawTrip)
        self.hand.delete_relation(self.hand.ExtractStop)
        self.hand.delete_relation(self.hand.ExtractRoute)
        self.hand.delete_relation(self.hand.ExtractUser)
        self.hand.delete_relation(self.hand.GTFSStop)
        self.hand.delete_relation(self.hand.GTFSRoute)

        # Finalisation
        end = time.time()
        print('Raw DB Established:', round(end-strt, 4), 'sec')
        return end-strt

    def raw_data_input(self, raw_file):
        """ Handles input of raw data in Raw SQLite DB. Assumes GTFS stop &
        route data stored as 'Stops_Raw.txt' & 'Routes_Raw.txt'

        :param raw_file: Name of raw trip data file at set directory
        """
        start = time.time()
        self.hand.new_raw_session(self.direct + 'Raw' + self.db_name)
        # Data Input/Extraction
        self.hand.new_rawtrip_file_core(self.direct+raw_file)
        self.hand.new_gtfsstop_file_core(self.direct+'Stops_Raw.txt')
        self.hand.new_gtfsroute_file_core(self.direct+'Routes_Raw.txt')
        self.hand.extract_all()

        # Error Checking
        stop_error = self.hand.stop_compare()
        route_error = self.hand.route_compare()

        # Finalisation
        end = time.time()
        print('Raw Data Input:', round(end-start, 4), 'sec')
        return stop_error, route_error, end-start

    def stop_analysis(self, stop_er):
        """ Handles the analysis of missing stop data in GTFS records
        :param stop_er - List of all stops present in trip data but not GTFS
        """
        strt = time.time()
        self.hand.new_raw_session(self.direct + 'Raw' + self.db_name)
        # Missing stops analysis
        fhand = open(self.direct+'Stops_PreProcess_Error.txt', 'w')
        for line in stop_er:
            fhand.write("{0}\n".format(line))
        fhand.close()
        self.hand.stop_tripCount(self.direct+'Stops_PreProcess_Error.txt',
                                 self.direct+'Stops_PreProcess_Error_Count.txt')
        # Finalisation
        end = time.time()
        print('Missing Stop Output + Count:', round(end-strt, 4), 'sec')
        return end-strt

    def raw_data_output(self):
        """ Handles the output of trip, user, stop & route data """
        start = time.time()
        self.hand.new_raw_session(self.direct + 'Raw' + self.db_name)
        self.hand.trip_output(self.direct + 'Trips_PreProcess.txt')
        self.hand.user_output(self.direct + 'Users_PreProcess.txt')
        self.hand.route_output(self.direct + 'Routes_PreProcess.txt')
        self.hand.stop_output(self.direct + 'Stops_PreProcess.txt')

        # Finalisation
        end = time.time()
        print('Raw Data Output', round(end - start, 4), 'sec')
        return end-start


class InputDataManagement(object):
    """ Class to handle Main Data Module in SmartTAP """
    def __init__(self, direct, db_name):
        """ Initialises InputControl class
        :param direct - input & output folder directory
        :param db_name - database root name"""
        self.direct = direct
        self.db_name = db_name
        self.hand = InpMod.InputControl()

    def main_database(self):
        """ Creation of new Main SQLite DB & deletion of existing data """
        start = time.time()
        # DB/Session Establishment
        self.hand.new_main_database(self.direct+self.db_name)
        self.hand.new_main_session(self.direct+self.db_name)

        # Old Data Deletion
        self.hand.delete_relation(self.hand.Stop)
        self.hand.delete_relation(self.hand.Route)
        self.hand.delete_relation(self.hand.RouteStop)
        self.hand.delete_relation(self.hand.Users)
        self.hand.delete_relation(self.hand.TripData)

        # Finalisation
        end = time.time()
        print('Main DB Established:', round(end-start, 4), 'sec')
        return end-start

    def main_data_input(self):
        """ Handles input of data from RawDataModule. Filenames based on
        those output from RawDataManagement.raw_data_output() function """
        start = time.time()
        self.hand.new_main_session(self.direct + self.db_name)

        # Stop Data
        strt1 = time.time()
        erS, trS, prS = self.hand.new_stop_file_core(
            self.direct+'Stops_PreProcess.txt')
        print('# Stops:', trS, '# Errors:', erS, '% Total:', prS)
        end1 = time.time()
        print('Stop Data Input:', round(end1-strt1, 8), 'sec')

        # Route Data
        strt2 = time.time()
        erR, trR, prR = self.hand.new_route_file_core(
            self.direct+'Routes_PreProcess.txt')
        print('# Routes:', trR, '# Errors:', erR, '% Total:', prR)
        end2 = time.time()
        print('Route Data Input:', round(end2-strt2, 8), 'sec')

        # User Data
        strt3 = time.time()
        erU, trU, prU = self.hand.new_user_file_core(
            self.direct+'Users_PreProcess.txt')
        print('# Users:', trU, '# Errors:', erU, '% Total:', prU)
        end3 = time.time()
        print('User Data Input:', round(end3 - strt3, 8), 'sec')

        # Trip Data
        strt4 = time.time()
        erT, trT, prT, er_dict = self.hand.new_trip_file_core(
            self.direct+'Trips_PreProcess.txt', self.direct+'Trips_Error.txt')
        print('# Trips:', trT, '# Errors:', erT, '% Total:', prT)
        print('Error breakdown:\n', er_dict)
        end4 = time.time()
        print('Trip Data Input:', round(end4 - strt4, 8), 'sec')

        # Finalisation
        end = time.time()
        print('Data Input:', round(end-start, 8), 'sec')
        return [(erS, trS, prS), (erR, trR, prR), (erU, trU, prU),
                (erT, trT, prT), (end-start), er_dict]

    def main_data_get(self):
        """ Returns all data in Main DB """
        start = time.time()
        self.hand.new_main_session(self.direct + self.db_name)
        (stops, routes, users,
         trips) = (self.hand.get_stops(), self.hand.get_routes(),
                   self.hand.get_users(), self.hand.get_trips())
        print('{0}\n\n{1}\n\n{2}\n\n{3}\n'.format(stops, routes, users, trips))
        end = time.time()
        print('Display DB Data:', round(end-start, 8), 'sec')

    def get_stops(self):
        """ Returns stop data from Main DB """
        start = time.time()
        self.hand.new_main_session(self.direct + self.db_name)
        stops = self.hand.get_stops()
        print(stops)
        end = time.time()
        print('Display Stop Data:', round(end-start, 8), 'sec')
        return stops


class AnalysisDataManagement(object):
    """ Class to handle Analysis Module in SmartTAP """
    def __init__(self, direct, db_name):
        self.direct = direct
        self.db_name = db_name
        self.hand = AnlyMod.AnalysisControl()

    def anly_database(self):
        """ Creation of new Analysis SQLite DB & deletion of existing data """
        start = time.time()
        # DB/Session Establishment
        self.hand.new_analysis_db(self.direct+'Anly'+self.db_name)
        self.hand.new_analysis_session(self.direct+'Anly'+self.db_name)
        self.hand.new_main_session(self.direct+self.db_name)

        # Old Data Deletion
        self.hand.delete_relation(self.hand.StopAnBrd)
        self.hand.delete_relation(self.hand.StopAnAli)

        # Finalisation
        end = time.time()
        print('Analysis DB Established:', round(end-start, 4), 'sec')
        return end-start

    def jrny_analysis(self, dates, users):
        """ Analyses journey behaviour for entire data set, or a selection of
        users and/or dates
        :param dates - List of dates to analyse, for no analysis eave as 0
        :param users - Filename for .txt file with userIDs for analysis """
        start = time.time()
        (trip_count, jrny_count) = self.hand.journey_analysis(
            self.direct+'Analysis_Journey.csv', dates, users)
        end = time.time()
        print('Journey Analysis:', round(end-start, 4), 'sec')
        return trip_count, jrny_count, end-start

    def stop_usage_summary(self):
        """ Count boarding and alighting from trips for each stop """
        start = time.time()
        self.hand.stop_usage_summary(self.direct + 'Analysis_Stop_Usage.csv')
        end = time.time()
        print('Basic Trip-to-Stop Analysis:', round(end-start, 4), 'sec')
        return end-start

    def stop_usage_detail(self):
        """ Boarding and alighting based on stopID, routeID, userType,
        date & hour """
        start1 = time.time()
        brd_data, ali_data = self.hand.stop_usage_detail()
        end1 = time.time()
        print('Trip to Stop Detail:', end1-start1, 'sec')

        start2 = time.time()
        self.hand.input_stop_usage(brd_data, ali_data)
        end2 = time.time()
        print('Analysis Data Input:', end2 - start2, 'sec')
        return end1-start1, end2-start2

    def orig_dest_v2(self):
        """ Improved OD-Matrix calculation function """
        print('OD-Matrix V2 Begun')
        start = time.time()
        out_file = self.direct+'Analysis_OD_Matrix.csv'
        self.hand.origin_destination_v2(out_file)
        end = time.time()
        print('OD-Matrix Calc:', round(end-start, 4), 'sec')
        return end-start

    def route_usage_summary(self):
        start = time.time()
        self.hand.route_usage_summary(self.direct + 'Analysis_Route_Usage.csv')
        end = time.time()
        print('Route Usage Analysis:', round(end-start, 8), 'sec')
        return end-start

    def route_usage_detail(self):
        start = time.time()
        self.hand.route_usage_detail(self.direct+'Analysis_Route_Usage_Det.csv')
        end = time.time()
        print('Detailed Route Usage Analysis:', round(end-start, 8), 'sec')
        return end-start
