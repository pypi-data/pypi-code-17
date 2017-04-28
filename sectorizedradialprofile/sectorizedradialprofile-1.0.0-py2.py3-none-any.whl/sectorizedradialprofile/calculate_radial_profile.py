
import numpy as np

class CalculateRadialProfile(object):
    
    radial_profile = []
    
    def __init__(self, data=[], center={}, angle_range={}):
        '''
        Arguments:
        
        - data: numpy 2D array
        - center: dictionary that defines the center position of the circle
              ex: 
              center = {'x0': 0.5,
                        'y0': 1.1}
        - angle_range: dictionary that defines the sector in degrees to consider. Angle 0 is
        the top vertical and going clockwise. So angle range is [0, 360[
        '''
        
        self.data = data
        self.center = center
        self.angle_range = angle_range

        if center:
            try:
                x0 = center['x0']
                y0 = center['y0']
                self.x0 = x0
                self.y0 = y0
            except:
                raise ValueError

        if angle_range:
            try:
                from_angle = angle_range['from']
                to_angle = angle_range['to']
                self.from_angle = from_angle
                self.to_angle = to_angle
            except:
                raise ValueError

    def calculate(self):
        '''performs the radial profile calculation'''
        
        if self.data == []:
            return
        
        self.calculate_array_size()
        #self.convert_angles_to_radians()
        self.calculate_pixels_radius()
        self.calculate_pixels_angle_position()
        self.turn_off_data_outside_angle_range()
        self.sort_indices_of_radius()
        self.sort_radius()
        self.sort_data_by_radius_value()
        self.calculate_radius_bins_location()
        self.calculate_radius_bins_size()
        self.calculate_profile()
        
    def calculate_profile(self):
        '''calculate the final profile'''

        # cumulative sum to figure out total counts for each radii bin
        cumulative_sum = np.cumsum(self.data_sorted_by_radius, dtype=np.float64)
        
        # sum of counts for each radii bin
        total_counts_bin = cumulative_sum[self.radius_bins_location[1:]] - \
            cumulative_sum[self.radius_bins_location[:-1]]

        # calculate profile
        self.radial_profile = total_counts_bin / self.radius_bins_size
        
    def calculate_radius_bins_size(self):
        '''define the size of each radius bin size'''
        self.radius_bins_size = self.radius_bins_location[1:] - self.radius_bins_location[:-1]
        
    def calculate_radius_bins_location(self):
        '''define an array of indices that show the integer radius jumps'''
        _integer_radius = self.sorted_radius.astype(np.int32)
        _delta_r = _integer_radius[1:] - _integer_radius[:-1]
        self.radius_bins_location = np.where(_delta_r)[0]
        
    def sort_data_by_radius_value(self):
        '''sort the working data by radius indices'''
        self.data_sorted_by_radius = self.working_data.flat[self.sorted_radius_indices]
        
    def sort_radius(self):
        '''sort the radius array'''
        self.sorted_radius = self.radius_array.flat[self.sorted_radius_indices]
        
    def sort_indices_of_radius(self):
        '''sort the indices of the radius array'''
        sort_indices = np.argsort(self.radius_array.flat)
        self.sorted_radius_indices = sort_indices
        
    def turn_off_data_outside_angle_range(self):
        '''using the angle range provided and the angle value of each pixels,
        this algorithm replace all the initial data by 0 outside the range specified'''
        left_angles_indices = self.array_angle_deg >= self.from_angle
        right_angles_indices = self.array_angle_deg <= self.to_angle
        
        angles_to_keep = np.logical_and(left_angles_indices, right_angles_indices)
        angles_to_not_keep = np.invert(angles_to_keep)
        
        working_data = np.array(self.data)
        working_data[angles_to_not_keep] = 0
        
        self.working_data = working_data

    def calculate_array_size(self):
        '''retrieve the width and height of the array'''
        [self.height, self.width] = np.shape(self.data)
        
    def calculate_pixels_angle_position(self):
        '''determine the angle position related to the top vertical center of
        each pixel in radians'''
        complex_array = (self.height - self.y_index - self.y0) + 1j * \
            (self.x_index - self.x0)
        array_angle_deg = np.angle(complex_array, deg=True)
        
        #removing all negative angles -> [0, 360[
        array_angle_deg_pos = np.array(array_angle_deg)
        for _y in np.arange(self.height):
            for _x in np.arange(self.width):
                _value = array_angle_deg[_y, _x]
                if _value < 0:
                    array_angle_deg_pos[_y, _x] = 2 * 180 + _value

        self.array_angle_deg = array_angle_deg_pos
        
    def calculate_pixels_radius(self):
        '''calculate radii of all pixels '''
        self.y_index, self.x_index = np.indices(self.data.shape)
        radius = np.sqrt((self.x_index-self.x0)**2 + (self.y_index-self.y0)**2)      
        self.radius_array = radius
    
    #def convert_angles_to_radians(self):
        #'''convert from degress to radians the angles. This is necessary
        #to evaluate the angle range with the the angle position of each pixel'''
        #self.from_angle_rad = np.deg2rad(self.from_angle)
        #self.to_angle_rad = np.deg2rad(self.to_angle)