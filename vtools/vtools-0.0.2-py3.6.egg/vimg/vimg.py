####################################################################################################
########################################### vtools.vimg ############################################
############################################# vimg.py ##############################################
####################################################################################################
######################################## Import Statements #########################################
import numpy as np
import cv2
import atexit
from .config import __IDENT__
from .colors import *


####################################################################################################
############################################# CLASSES ##############################################
class vImg(np.ndarray):
    def __new__(cls, imgFn=None, **kwargs):
        """Initiates a vImg object using np.ndarray as base class. The vImg object extends the array
        to allow for some basic image modification methods to be executed on the base class.
        Parameters:
            imgFn = string, path to image
            **kwargs (optional, only color may be used if img is supplied)
            img    : numpy np.ndarray type
            height : in pixels, height of the blank image
            width  : in pixels, width of the blank image
            color  : in RGB tuple, the bg color for the blank image (default: black)
            height
        """

        def blank(height, width, color=(0, 0, 0)):
            """Creates a blank image
            Parameters:
                height = in pixels, height of the blank image
                width = in pixels, width of the blank image
                color = in RGB tuple, the bg color for the blank image (default: black)
                remember, in OpenCV rgb values are stored as (B,G,R)
            """
            blank_image = np.zeros((height, width, 3), dtype='uint8')
            color = (color[2], color[1], color[0])
            if color != BLACK: blank_image[:, :] = color
            return blank_image

        if imgFn is None:
            try:
                if kwargs.get('img', None) is not None:
                    img = kwargs['img']
                else:
                    img = blank(kwargs['height'], kwargs['width'], kwargs.get('color', BLACK))
                obj = np.asarray(img).view(cls)
                obj.__h, obj.__w = obj.shape[:2]
                obj.__center = (obj.w // 2, obj.h // 2)
                obj.__color = kwargs.get('color', BLACK)
                return obj
            except KeyError:
                str_err = "KeyError: If 'image' argument not provided, keyword arg(s) for "
                str_err += ('width and height ' if not kwargs.get('height', None) and not kwargs.get('width', None)
                            else 'height ' if not kwargs.get('height', None)
                            else 'width ' if not kwargs.get('width', None)
                            else 'unknown property ')
                str_err += 'must be provided (color is optional).'
                print(str_err)
                return

        try:
            obj = np.asarray(cv2.imread(imgFn)).view(cls)
            obj.imgFn = imgFn
            obj.__h, obj.__w = obj.img.shape[:2]
        except:
            raise ValueError("Unable to open file at {}".format(imgFn))
            return

        obj.__center = (obj.__w // 2, obj.__h // 2)
        obj.__color = kwargs.get('color', (0, 0, 0))
        obj.__title = kwargs.get('title', None)
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.__h = getattr(obj, '__h', None)
        self.__w = getattr(obj, '__w', None)
        self.__center = getattr(obj, '__center', None)
        self.__color = getattr(obj, '__color', None)
        self.__title = getattr(obj, '__title', None)

        if self.__title is None:
            self.__title = 'img' + next(__IDENT__)




    def __array_wrap__(self, out_arr, context=None):
        """__array_wrap__ gets called at the end of numpy ufuncs and
        other numpy functions, to allow a subclass to set the type of
        the return value and update attributes and metadata"""
        self.__h = getattr(out_arr, '__h', None)
        self.__w = getattr(out_arr, '__w', None)
        self.__center = getattr(out_arr, '__center', None)
        self.__color = getattr(out_arr, '__color', None)
        self.__title = getattr(out_arr, '__title', None)

        if self.__title is None:
            self.__title = 'img' + next(__IDENT__)

        return np.ndarray.__array_wrap__(self, out_arr, context)


    def __eq__(self, other):
        if np.array_equal(self, other): return True

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, val):
        self.__h = val

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, val):
        self.__w = val

    @property
    def height(self):
        return self.__h

    @height.setter
    def h(self, val):
        self.__h = val

    @property
    def width(self):
        return self.__w

    @w.setter
    def width(self, val):
        self.__w = val

    @property
    def center(self):
        if not self.__center:
            self.h, self.w = self.shape[:2]
            self.__center = (self.w // 2, self.h // 2)
        return self.__center

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, val):
        self.__color = val

    @property
    def title(self):
        if not self.__title:
            self.title = 'img' + next(__IDENT__)
        return self.__title

    @title.setter
    def title(self, val):
        assert isinstance(val,str), 'Title must be of type string'

    ####################################################################################################
    ########################## Reused some of Dr. Adrian Rosebrock's code and ##########################
    ########################### comments from his excellent package imutils ############################
    #########################  and book 'Practical Python and OpenCV' below.  ##########################

    def BGR2RGB(self):
        image = cv2.cvtColor(self.copy(), cv2.COLOR_BGR2RGB)
        return vImg(img=image)

    def BGR2RGB(self):
        image = cv2.cvtColor(self.copy(), cv2.COLOR_RGB2BGR)
        return vImg(img=image)

    def gray(self):
        """ function that returns a grayscale copy of the vImg object """
        gray = self.copy()
        cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        return vImg(img=gray)

    def translate(self, x, y):
        """ function that returns translated (shifted by x and y pixels) image
        x : int, number of pixels to move the image horizontally (positive right, negative left)
        y : int, number of pixels to move the image vertically (positive down, negative up)
        """
        # Define the translation matrix and perform the translation
        M = np.float32([[1, 0, x], [0, 1, y]])
        shifted = cv2.warpAffine(self, M, (self.shape[1], self.shape[0]))
        # Return the translated image
        return vImg(img=shifted)
    
    def rotate(self, angle = 90, center = None, scale = 1.0):

        if not center: center = self.center
        # Perform the rotation
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(self, M, (self.w, self.h))

        # Return the rotated image
        return vImg(img=rotated)
    
    def resize(self, width = None, height = None, inter = cv2.INTER_AREA):
        """ function that returns a resized image based on a given width, height, or both.
        Maintains the aspect ratio of the image if given only one dimension.
        width  : int, optional, width in pixels for the resized image
        height : int, optional, height in pixels for the resized image
        inter  : cv2 CONSTANT, optional, interpolation method
        Valid values for inter:
        cv2.INTER_AREA (default)
        cv2.INTER_NEAREST
        cv2.INTER_CUBIC
        cv2.INTER_LINEAR
        cv2.INTER_LANCZOS4
        """
        # initialize the dimensions of the image to be resized and grab the image size
        dim = None
        (h, w) = self.shape[:2]

        # if both the width and height are None, then return the original image
        if width is None and height is None:
            return vImg(img=self)

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(self.copy(), dim, interpolation=inter)

        # set the new state and img of the resized img
        return vImg(img=resized)

    def threshold(self, T, k = 5, inverse = True):
        """ We will apply binary thresholding from the current image object and return
        the second result i.e. the threshold map (extremely basic)
        T : int, threshold pixel intensity
        k : kernel size in square pixels for gaussian blur, default to 5
        inverse: bool, whether or not to return an inverse binary threashold, default YES
        """
        # The value of k must be odd so that there's a center pixel in the matrix
        if k % 2 == 0: raise ValueError(f'k must be an odd number... not {k}')

        # First, convert the color scale of the image to grayscale, then apply a gaussian blur
        image = cv2.cvtColor(self.copy(), cv2.COLOR_BGR2GRAY)
        gauss = cv2.GaussianBlur(image, (k,k), 0)

        # Next, apply the threshold to the image
        thresh_bin = cv2.THRESH_BINARY if inverse is not True else cv2.THRESH_BINARY_INV
        thresh = cv2.threshold(gauss, T, 255, thresh_bin)[1]

        # Finally, return the result
        return vImg(img=thresh)

    def adaptiveThreshold(self, adaptive_method, neighborhood_size, k = 5, C = 0, inverse = False):
        """ We will apply adaptive thresholding to the image object and return a threshold map
        based off of a given neighborhood size.
        adaptive_method   : cv2 constant that represents which adaptive thresholding method we will
                            use (e.g. cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        neighborhood_size : int, size of the neighborhood in which to evaluate small areas of
                            pixels in order to find an optimal value of T to apply thresholding
        k                 : int, kernel size in square pixels for gaussian blur, default to 5
        C                 : int, subtracted from the mean, giving us granular control of the adaptive
                            thresholding process, default to 0
        inverse           : bool, value representing whether or not the threshold constant used will
                            be inverse or normal. Inverse is default since it's commonly used for
                            masking.
        """
        # The value of k must be odd so that there's a center pixel in the matrix
        if k % 2 == 0: raise ValueError(f'k must be an odd number... not {k}')

        # First, convert the color scale of the image to grayscale, then apply a gaussian blur
        image = cv2.cvtColor(self.copy(), cv2.COLOR_BGR2GRAY)
        gauss = cv2.GaussianBlur(image, (k,k), 0)

        # Next, apply the threshold to the image
        thresh_bin = cv2.THRESH_BINARY if not inverse else cv2.THRESH_BINARY_INV

        thresh = cv2.adaptiveThreshold(gauss, 255, adaptive_method, thresh_bin, neighborhood_size, C)
        return vImg(img=thresh)

    def autoCanny(self, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(self)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(self, lower, upper)

        # return the edged image
        return vImg(img=edged)

    def simpleContours(self, quantity = cv2.RETR_EXTERNAL, complexity = cv2.CHAIN_APPROX_SIMPLE):
        """Performs simple cv2.findContours operation using common but overridable default 
           parameters on a vImg object, returns a list of vContour
        
        quantity    : cv2.RETR_EXTERNAL (default), also could be: cv2.RETR_LIST, cv2.RETR_COMP, 
                      and cv2.RETR_TREE
        complexity  : cv2.CHAIN_APPROX_SIMPLE (default), also could be: cv2.CHAIN_APPROX_NONE
        
        Passes the second element returned from cv2.findContours to the vContour class's fromList
        builder. This is because the first element returned by cv2.findContours is a 'destroyed'
        version of the image passed to it.
        """
        return vContour.fromList(cv2.findContours(self.copy(), quantity, complexity)[1])

    def evalContours(self, cnts = None):
        """This function exists to make it easier to evaluate contours in an image. Calling this
        function and supplying a list of contours iterates through the list of contours and
        identifies them one at a time on the image while simultaneously displaying useful
        simple and advanced contour properties in the console. Very useful for determining if 
        contour analysis may be used effectively in a given application.
        
        Not generally applicable or useful in a production environment.
        
        cnts : a list of vContour objects (use the simpleContours method to easily generate a list
               of vContours)
        """

        if cnts is None:
            cnts = self.simpleContours()

        assert hasattr(cnts, '__iter__') and isinstance(cnts[0], vContour), 'Must be iterable of vContours'
        img = self.copy()

        for i, c in enumerate(cnts, 1):
            cv2.drawContours(img, [c], -1, WHITE, 1)
            cv2.putText(img, f'#{i}', (c.x, c.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cvtColor(YELLOW), 2)
            print("""Shape #{i} @ x({x1},{x2}) y({y1}, {y2})
            --------------------------------------------------------------
            width: {width} height: {height}
            Aspect Ratio is (image width / image height): {aspect_ratio:.2f}
            Contour Area is: {area:.2f}
            Bounding Box Area is: {bbarea:.2f}
            Convex Hull Area is: {hull_area:.2f}
            Solidity (Contour Area / Convex Hull Area) is: {solidity:.2f} 
            Extent (Contour Area / Bounding Box Area) is: {extent:.2f}
            Center is located at: {center}""".format(i=i, x1=c.x, x2=c.x2, width=c.width, y1=c.y, y2=c.y2,
                                                     height=c.height,
                                                     aspect_ratio=c.aspect_ratio, area=c.area,
                                                     bbarea=c.width * c.height,
                                                     hull_area=c.hull_area, solidity=c.solidity, extent=c.extent,
                                                     center=c.center))
            cv2.imshow(self.title, img)
            cv2.waitKey(0)
        atexit.register(cv2.destroyAllWindows)

    def show(self, title = None, wait = 0):
        if not title:
            title = self.title
        cv2.imshow(title, self)
        cv2.waitKey(wait)
        atexit.register(cv2.destroyAllWindows)

####################################################################################################
########################################## BEGIN vContour ##########################################

class vContour(np.ndarray):
    """ The vContour class is a helper class for extending contours identified by opencv"""
    def __new__(cls, cnt):
        return np.asarray(cnt).view(cls)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.__x, self.__y, self.__w, self.__h = cv2.boundingRect(obj)
        self.__x2 = self.__x + self.__w
        self.__y2 = self.__y + self.__h
        self.__aspect_ratio = self.__w / self.__h
        self.__perim = None
        self.__area = None
        self.__extent = None
        self.__hull = None
        self.__hull_area = None
        self.__solidity = None
        self.__center = None



    def __array_wrap__(self, out_arr, context=None):
        """__array_wrap__ gets called at the end of numpy ufuncs and
        other numpy functions, to allow a subclass to set the type of
        the return value and update attributes and metadata"""
        self.__x, self.__y, self.__w, self.__h = cv2.boundingRect(out_arr)
        self.__x2 = self.__x + self.__w
        self.__y2 = self.__y + self.__h
        self.__aspect_ratio = self.__w / self.__h
        self.__perim = None
        self.__area = None
        self.__extent = None
        self.__hull = None
        self.__hull_area = None
        self.__solidity = None
        # return image
        return np.ndarray.__array_wrap__(self, out_arr, context)

    @classmethod
    def fromList(cls, cnts):
        """ fromList is a classmethod that can be used to return a generator of vContour objects
            from a list of opencv contours returned from the cv2.findContours method"""
        if isinstance(cnts, list):
            return (cls(c) for c in cnts)
        else:
            raise ValueError('fromList() constructor requires a list of contours of type nd.array') from None
    def __eq__(self, other):
        return True if np.array_equal(self, other) else False

    @property
    def x(self):
        return self.__x

    @property
    def x2(self):
        return self.__x2

    @property
    def y(self):
        return self.__y

    @property
    def y2(self):
        return self.__y2

    @property
    def w(self):
        return self.__w

    @property
    def h(self):
        return self.__h

    @property
    def width(self):
        return self.__w

    @property
    def height(self):
        return self.__h

    @property
    def center(self):
        if self.__center is None:
            self.center = ((self.__x + self.__x2) / 2, (self.__y + self.__y2) / 2)
        return self.__center

    @center.setter
    def center(self, val):
        self.__center = val

    @property
    def aspect_ratio(self):
        return self.__aspect_ratio

    @property
    def perim(self):
        if self.__perim is None:
            self.perim = cv2.arcLength(self, True)
        return self.__perim

    @perim.setter
    def perim(self, val):
        self.__perim = val

    @property
    def area(self):
        if self.__area is None:
            self.area = cv2.contourArea(self)
        return self.__area

    @area.setter
    def area(self, val):
        self.__area = val

    @property
    def extent(self):
        if self.__extent is None:
            self.extent = self.area / (self.width * self.height)
        return self.__extent

    @extent.setter
    def extent(self, val):
        self.__extent = val

    @property
    def hull(self):
        if self.__hull is None:
            self.hull = cv2.convexHull(self)
        return self.__hull

    @hull.setter
    def hull(self, val):
        self.__hull = val

    @property
    def hull_area(self):
        if self.__hull_area is None:
            self.hull_area = cv2.contourArea(self.hull)
        return self.__hull_area

    @hull_area.setter
    def hull_area(self, val):
        self.__hull_area = val

    @property
    def solidity(self):
        if self.__solidity is None:
            self.solidity = self.area / self.hull_area
        return self.__solidity

    @solidity.setter
    def solidity(self, val):
        self.__solidity = val

####################################################################################################
######################################### HELPER FUNCTIONS #########################################

def cvtColor(color):
    """Convert RGB to BGR color or vice versa"""
    return color[::-1]
