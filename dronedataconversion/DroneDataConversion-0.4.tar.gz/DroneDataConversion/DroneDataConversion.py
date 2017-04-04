'''
Created on 12.06.2016

@author: johanneskinzig
@license: Apache License, Version 2.0
@version: 0.4

'''

# -*- coding: utf-8 -*-

import sys
import json
import gpxpy
import gpxpy.gpx
from geopy.distance import vincenty, great_circle
from geopy.geocoders import Nominatim
from datetime import timedelta
import dateutil.parser as parser
import os

class BebopFlightDataManager():
    
    #####################################################################
    #    Methods mostly used inside this library are helper functions   #
    #####################################################################
    
    def __init__(self, pud_file):
        """Constructor for BebopFlightDataManager. Load the PUD/JSON file for later parsing"""
        # opens the file with proper error handling
        try:
            self.json_file = open(pud_file, "r") # also known as PUD file, because on the drones filesystem the file has the .pud extension
        except IOError:
            sys.exit("File not found! Aborting!") # exit with code 1 - Error
        
        # reading in the file
        self.json_string = self.json_file.read()
        # close file after reading
        self.json_file.close()
        
        # extract filename from path (only filename wanted, path is cut of !!!)
        pud_path, pud_name = os.path.split(pud_file)
        self.raw_file_name = pud_name
        # extract diagnostic information about the PUD/JSON file
        self.json_string = json.loads(self.json_string)
        self.details_header_array = self.json_string['details_headers']
        self.details_data_array_contains_list = self.json_string['details_data']
        self.product_name = self.json_string['product_name']
        self.product_id = self.json_string['product_id']
        self.json_file_version = self.json_string['version']
        self.product_software_version = self.json_string['software_version']
        self.product_hardware_version = self.json_string['hardware_version']
        self.product_serial_number = self.json_string['serial_number']
        self.controller_model = self.json_string['controller_model']
        self.controller_position = []
        self.controller_position.append(self.json_string['gps_latitude'])
        self.controller_position.append(self.json_string['gps_longitude'])
        self.flight_duration = self.json_string['run_time']
        self.flight_data_date = self.json_string['date']

    def calculate_distance_traveled_vincenty(self):
        '''Calculate the distance traveled using vincenty distance.'''
        distance_traveled = 0
        for flight_data_entry in self.details_data_array_contains_list:
            # if latitude and longitude are both 500.0 at a point, this means there is no GPS signal
            if flight_data_entry[9] == 500.0 and flight_data_entry[8] == 500.0:
                continue # skip one interation
            else:
                if distance_traveled == 0:
                    # in first iteration only store 'current_location' as 'location before', do not calculate a distance
                    # identifier when first iteration is successfully performed: set distance_traveled to a bit higher than 0
                    location_before = (flight_data_entry[9], flight_data_entry[8])
                    distance_traveled = 0.0001
                    continue # skip iteration, in next iteration processing will continue in the "else" branch
                else:
                    current_location = (flight_data_entry[9], flight_data_entry[8])
                    distance_traveled = distance_traveled + vincenty(location_before, current_location).meters
                    location_before = current_location
        return distance_traveled
    
    def calculate_distance_traveled_gc(self):
        ''' Calculate the distance traveled using great circle distance.
        '''
        distance_traveled = 0
        for flight_data_entry in self.details_data_array_contains_list:
            # if latitude and longitude are both 500.0 at a point, this means there is no GPS signal
            if flight_data_entry[9] == 500.0 and flight_data_entry[8] == 500.0:
                continue # skip one interation
            else:
                if distance_traveled == 0:
                    # in first iteration only store 'current_location' as 'location before', do not calculate a distance
                    # identifier when first iteration is successfully performed: set distance_traveled to a bit higher than 0
                    location_before = (flight_data_entry[9], flight_data_entry[8])
                    distance_traveled = 0.0001
                    continue # skip iteration, in next iteration processing will continue in the "else" branch
                else:
                    current_location = (flight_data_entry[9], flight_data_entry[8])
                    distance_traveled = distance_traveled + great_circle(location_before, current_location).meters
                    location_before = current_location
        return distance_traveled
        
    
    #####################################################################
    #         Methods mostly used outside this library                  #
    #####################################################################

    def display_diagnostic_information_debug(self):
        '''Extract all the necessary information from the pud/json file.
            Calculate important information which is not stored in the pud file. Return a list with 25 elements of type string. 
            Include human readable descriptions for every data field.'''
        diagnostic_information = []
        diagnostic_information.append('--- Diagnostic File Information: ---')
        diagnostic_information.append('Raw Data File Name: ' + str(self.raw_file_name))
        diagnostic_information.append('JSON File Version: ' + str(self.json_file_version))
        diagnostic_information.append('Length of header fields: ' + str(len(self.details_header_array)))
        diagnostic_information.append('Length of detailed list: ' + str(len(self.details_data_array_contains_list)))
        diagnostic_information.append('Length of single flight-data-list: ' + str(len(self.details_data_array_contains_list[0])))
        diagnostic_information.append('--- Diagnostic Drone Information: ---')
        diagnostic_information.append('Product Name: ' + str(self.product_name))
        diagnostic_information.append('Product ID: ' + str(self.product_id))
        diagnostic_information.append('Product Software Version: ' + str(self.product_software_version))
        diagnostic_information.append('Product Hardware Version: ' + str(self.product_hardware_version))
        diagnostic_information.append('Product Serial Number: ' + str(self.product_serial_number))
        diagnostic_information.append('Controller Model: ' + str(self.controller_model))
        diagnostic_information.append('--- Diagnostic Flight Information: ---')
        diagnostic_information.append('Pilot Location: ' + str(self.controller_position).strip('[]'))
        diagnostic_information.append('City nearby: ' + str(self.get_nearest_city(str(self.controller_position).strip('[]'))))
        diagnostic_information.append('Flight duration: ' + str(self.flight_duration) + 'ms' + ' => ' + str(float(self.flight_duration)/1000/60) + ' Minutes')
        diagnostic_information.append('Flight Data Timestamp: ' + str(self.flight_data_date))
        diagnostic_information.append('Distance traveled (vincenty): ' + str(self.calculate_distance_traveled_vincenty()) + 'm')
        diagnostic_information.append('Distance traveled (great circle): ' + str(self.calculate_distance_traveled_gc())+ 'm')
        diagnostic_information.append('Max Altitude: ' + str(self.determine_max_altitude()) + 'm')
        diagnostic_information.append('Average speed: ' + str(self.determine_avg_speed()) + 'm/s')
        diagnostic_information.append('Battery used: ' + str(self.get_battery_percentage()) + '%')
        diagnostic_information.append('--- End of Diagnostics ---')
        
        print ("\n".join(diagnostic_information))
        return diagnostic_information
    
    def diagnostic_information_raw(self):
        '''Return diagnostic information as raw values, prepared for further processing.'''
        # define array
        diagnostic_information_list = []
        # city nearby - string
        diagnostic_information_list.append(self.get_nearest_city(str(self.controller_position).strip('[]')))
        # pilot_location - string
        diagnostic_information_list.append(str(self.controller_position))
        # date_time - string
        diagnostic_information_list.append(str(self.flight_data_date))
        # total_distance - mean of vincenty and gc - float
        diagnostic_information_list.append((float(self.calculate_distance_traveled_vincenty()) + float(self.calculate_distance_traveled_gc()))/2)
        # max altitude - float
        diagnostic_information_list.append(self.determine_max_altitude())
        # avg speed - float
        diagnostic_information_list.append(self.determine_avg_speed())
        # flight_duration - datetime
        diagnostic_information_list.append(float(self.flight_duration)/1000/60)
        # controller type - string
        diagnostic_information_list.append(str(self.controller_model))
        # drone_type - string
        diagnostic_information_list.append(str(self.product_name))
        # battery_usage
        diagnostic_information_list.append(self.get_battery_percentage())
        # raw_data_file_name
        diagnostic_information_list.append(self.raw_file_name)
        
        return diagnostic_information_list
        
    def determine_avg_speed(self):
        '''Calculate average speed of flight.'''
        speed_at_positions = []
        for flight_data_entry in self.details_data_array_contains_list:
            speed_at_positions.append(flight_data_entry[20])
        
        avg_speed = sum(speed_at_positions)/len(speed_at_positions)
        return avg_speed
    
    def determine_max_altitude(self):
        '''Calculate the maximum altitude.'''
        # max altitude helper variable
        max_altitude = 0.0
        # check each altitude datafiled out of all data fields
        for flight_data_entry in self.details_data_array_contains_list:
            # convert to meters, raw data is in milimeters
            flight_data_altitude_hr = flight_data_entry[18]/1000
            if flight_data_altitude_hr > max_altitude:
                max_altitude = flight_data_altitude_hr
            else:
                pass
        return max_altitude
    
    def get_nearest_city(self, coordinates_as_string):
        '''Perform a request to OSM geo database and return nearest city for pilot position.'''
        try:
            geolocator = Nominatim()
            location = geolocator.reverse(coordinates_as_string)
        except:
            return "-- Service not available --"
        
        identifier = ['town', 'city', 'village']
        for identity in identifier:
            try:
                city = location.raw['address'][identity]
                # convert string to utf8 because of locale dependent special characters
                return city.encode('utf-8')
            except:
                continue
        return "-- Valid identifier not found --"
    
    def get_battery_percentage(self):
        """Get battery percentage used for flight."""
        battery_remaining = self.details_data_array_contains_list[len(self.details_data_array_contains_list)-1][1]
        # Find current battery state; pud file is written to memory before battery monitor is booted, so the first values inside pud are "0"
        # Parse until the first value is greater than 0 and use it as battery level at takeoff
        battery_level_at_takeoff = None
        for bat_cur_state in self.details_data_array_contains_list:
            #print bat_cur_state[1]
            if int(bat_cur_state[1]) > 0:
                battery_level_at_takeoff = int(bat_cur_state[1])
                break
            
        battery_used = battery_level_at_takeoff - battery_remaining
        return battery_used


    def export_as_csv(self, destination_file_name):
        '''Export flight data as csv.'''
        destfile = open(destination_file_name, "a")
    
        for header in self.details_header_array:
            destfile.write(str(header) + ", ")
        destfile.write("\n")

        for flight_data_entry in self.details_data_array_contains_list:
            destfile.write(str(flight_data_entry) + "\n")

        destfile.close()
        print "Done - CSV file written to disk."
        
    def export_as_gpx(self, destination_file_name, gpx_track_name=None):
        '''Export flight data as GPX file. Write gpx file to disk.
        Keyword arguments:
        destination_file_name -- filename for the gpx file as string
        gpx_track_name -- (optional) name of gpx track
        '''
        # create new GPX object
        gpx_object = gpxpy.gpx.GPX()
        # Create first track in GPX object:
        gpx_object_track = gpxpy.gpx.GPXTrack(name=str(gpx_track_name))
        gpx_object.tracks.append(gpx_object_track)
        # Create first segment in our GPX track:
        gpx_object_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_object_track.segments.append(gpx_object_segment)
    
        for flight_data_entry in self.details_data_array_contains_list:
            # if latitude and longitude are both 500.0 at a point, this means there is no GPS signal
            if flight_data_entry[9] == 500.0 and flight_data_entry[8] == 500.0:
                continue # skip one iteration
            
            # convert mm to meters, in json/pud file altitude is given in mm
            flight_data_altitude_hr = flight_data_entry[18]/1000
            # if altitude is less than 0 set it to 0 because altitudes beyond ground do not make sense in the case of absolute altitudes
            if flight_data_altitude_hr < 0:
                flight_data_altitude_hr = 0 # human readable
            
            # prepare timestamp for gpx track, read from diagnostics
            date = (parser.parse(self.flight_data_date))
            # add the timestamp from pud
            gpx_timestamp = date + timedelta(seconds=(int(flight_data_entry[0]/1000)))
            gpx_object_segment.points.append(gpxpy.gpx.GPXTrackPoint(flight_data_entry[9], flight_data_entry[8], elevation=flight_data_altitude_hr, time=gpx_timestamp, speed=flight_data_entry[20]))
            
        destfile = open(destination_file_name, "a")
        destfile.write(gpx_object.to_xml())
        destfile.close()
        print "Done - GPX file written to disk."

    def takeoff_location_as_gpx(self, destination_file_name, waypoint_name=None):
        '''Export takeoff location as gpx waypoint'''
        # get date
        date = (parser.parse(self.flight_data_date))
        # create new GPX object
        gpx_object = gpxpy.gpx.GPX()        
        waypoint = gpxpy.gpx.GPXTrackPoint(self.controller_position[0], self.controller_position[1], time=date, name=str(waypoint_name), comment="Created with FlightReportManager")
        gpx_object.waypoints.append(waypoint)
        destfile = open(destination_file_name, "a")
        destfile.write(gpx_object.to_xml())
        destfile.close()
        print "Done - GPX Waypoint written to disk."
        
    def takeoff_location_as_csv(self, destination_file_name, waypoint_name=None):
        '''Export takeoff location as csv'''
        # str(self.controller_position).strip('[]'))
        destfile = open(destination_file_name, "a")
        destfile.write(str(waypoint_name) + ", " + str(self.controller_position).strip('[]') + ", " + str(parser.parse(self.flight_data_date)) + "\n")
        destfile.close()
        print "Done - CSV Waypoint written to disk."
    
# TODO: waypoint as kml
        
    def export_as_kml(self, destination_file_name):
        ''' Export as kml file. NOT IMPLEMENTED YET!!!'''
        # TODO: export as kml file
        pass

    def passFlightData(self):
        '''Passe flight data as lists for further processing; Pass:
        seconds airborne, latitude, longitude, altitude, speed, battery.
        '''
        pass_data_sec = [] # seconds airborne
        pass_data_lat = [] # gps latitude
        pass_data_lon = [] # gps longitude
        pass_data_alt = [] # altitude
        pass_data_spe = [] # speed
        pass_data_bat = [] # battery
        
        
        for flight_data_entry in self.details_data_array_contains_list:
            # if latitude and longitude are both 500.0 at a point, this means there is no GPS signal
            if flight_data_entry[9] == 500.0 and flight_data_entry[8] == 500.0:
                continue # skip one interation
            
            # convert mm to meters, in json/pud file altitude is given in mm
            flight_data_altitude_hr = flight_data_entry[18]/1000
            # if altitude is less than 0 set it to 0 because altitudes beyond ground do not make sense in the case of absolute altitudes
            if flight_data_altitude_hr < 0:
                flight_data_altitude_hr = 0 # human readable
            
            # extract the timestamp, convert ms to seconds
            flight_data_time_hr_sec = flight_data_entry[0]/float(1000)
            
            #print "Time", "Latitude", "Longitude", "Altitude (hr)",  "Speed (m/s)", "battery level (%)"
            #print flight_data_time_hr_sec, flight_data_entry[9], flight_data_entry[8], flight_data_altitude_hr, flight_data_entry[20], flight_data_entry[1]
            pass_data_sec.append(flight_data_time_hr_sec)
            pass_data_lat.append(flight_data_entry[9])
            pass_data_lon.append(flight_data_entry[8])
            pass_data_alt.append(flight_data_altitude_hr)
            pass_data_spe.append(flight_data_entry[20])
            pass_data_bat.append(flight_data_entry[1])

        return pass_data_sec, pass_data_lat, pass_data_lon, pass_data_alt, pass_data_spe, pass_data_bat

if __name__ == "__main__":
    """ For testing purpose """
    print("Init done")
    # demo and testing main capabilities
    testpud = BebopFlightDataManager("../DroneDataFiles/demo2.json")
    testpud.display_diagnostic_information_debug()
    testpud.export_as_gpx("../DroneDataFiles/demo2_track.gpx", gpx_track_name="DemoTrack")
    testpud.export_as_csv("../DroneDataFiles/demo2_track.csv")
    testpud.takeoff_location_as_csv("../DroneDataFiles/demo2_wpt.csv", waypoint_name="DemoWaypoint")
    testpud.takeoff_location_as_gpx("../DroneDataFiles/demo2_wpt.gpx", waypoint_name="DemoWaypoint")

    