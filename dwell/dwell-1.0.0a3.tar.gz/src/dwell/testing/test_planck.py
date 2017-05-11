import numpy as np
import dwell.planck as planck
import dwell.constants as const
import nose.tools
from dwell.testing import Testing

class test_planck(object):
    def __init__(self):
        """Initialize variables used to test planck library
        
        Initialized the variables needed to run the tests, these include
        solar temperature, wavelength range, solar_radius/orbit ratio,
        wavenumber range, acutal results from the integration, actual
        results form the series approximation.
        
        """
        self.test = Testing()
        self.solar_temp = 5750.
        self.wavelength = np.linspace(0.01,500,100000)
        self.scale = 0.004652**2 # (solar_rad/1.au)^2
        self.wavenumber = np.linspace(1,100000,1000)
        self.actual =  [1341.41, 1341.42]
        self.actual_cfst4 = [1341.41, 1341.42]
        
    def debug(self, expected, result,funcname):
        self.test.debug(funcname)

        print("expected between {0} and {1}".format(
            expected[0], expected[1]))
        print("{0} = {1}".format(funcname,result))

    def test_planck_wavelength(self):
        """Testing Planck wavelength with solar flux
        
        Calculates Planck function at a series of wavelengths, integrates to 
        get the total solar flux at the Earth, units of W/m^2
        
        """
        b = planck.planck_wavelength(self.wavelength,
                                     self.solar_temp)*self.scale
        tb= np.sum(b)*(self.wavelength[1]-self.wavelength[0])* np.pi
        self.debug(self.actual,tb,"planck_wavelength")
        assert (self.test.inRange(tb, self.actual))
    
    def test_planck_wavenumber(self):
        """Testing Planck wavenumber with solar flux
        
        Calculates Planck function at a series of wavenumbers, integrates to 
        get the total solar flux at the Earth, units of W/m^2.
        
        """
        b = planck.planck_wavenumber(self.wavenumber,
        self.solar_temp)*self.scale
        tb= np.sum(b)*(self.wavenumber[1]-self.wavenumber[0])* np.pi
        self.debug(self.actual,tb,"planck_wavenumber")
        assert (self.test.inRange(tb, self.actual))


    def test_st4(self):
        """Test sigma*T^4
        
        Tests st4 function with solar temperature, scaled by radius and orbit to 
        give solar flux at the Earth. Units of W/m^2
        
        """
        tb = planck.st4(self.solar_temp)*self.scale
        self.debug(self.actual,tb,"planck_st4")
        assert (self.test.inRange(tb, self.actual))
        
    def test_cfst4_wavenumber(self):
        """Testing wavenumber integrated planck
        
        Tests cfst4 with solar temperature, scaled by radius and orbit to 
        give solar flux at the Earth. Units of W/m^2
        
        """
        
        tb = planck.cfst4_wavenumber(self.wavenumber[0],
                                     self.wavenumber[-1],
                                     self.solar_temp)*self.scale
        self.debug(self.actual_cfst4,tb,"planck_cfst4_wavenumber")
        assert (self.test.inRange(tb, self.actual_cfst4))

        
    def test_cfst4_wavelength(self):
        """Testing wavelength integrated planck
        
        Tests cfst4 with solar temperature, scaled by radius and orbit to 
        give solar flux at the Earth. Units of W/m^2
        
        """
        tb = planck.cfst4_wavelength(self.wavelength[0],
                                     self.wavelength[-1],
                                     self.solar_temp)*self.scale
        self.debug(self.actual_cfst4,tb,"planck_cfst4_wavelength")
        assert (self.test.inRange(tb, self.actual_cfst4))

    def test_cfst4_a(self):
        """Testing cfst4 with finite limits
        
        Tests cfst4 with solar temperature, over finite wavelength limits
        form 1.0 to 100 micron, scaled by radius and orbit to 
        give solar flux at the Earth. Units of W/m^2
        
        """
        wl = 0.1
        wh = 1000.
        t = 300.
        error=1e-6
        ta = planck.cfst4_wavelength(wl,wh,t)
        tb = planck.cfst4_wavenumber(10000/wh,10000/wl,t)
        print("Comparing cfst4_wavelength and cfst4_wavenumber")
        print("cfst4_wavelength={0}".format(ta))
        print("cfst4_wavenumber={0}".format(tb))
        assert self.test.inRange((ta-tb),[-error,error])
        
    def allt(self):
        """Run all tests"""
        self.test_planck_wavelength()
        self.test_planck_wavenumber()
        self.test_st4()
        self.test_cfst4_wavenumber()
        self.test_cfst4_wavelength()
        self.test_cfst4_a()


if __name__=="__main__":
    c = test_planck()
    c.allt()
    
