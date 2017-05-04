from dwell.testing import Testing
import dwell.smoothing as sm
import numpy


class test_smoothing(object):
    def __init__(self):
        """Initialize variables used to test smoothing library
        """
        self.test = Testing()
    
    def test_oddbox(self):
        assert sm.oddbox("dummy",11) == 11
        assert sm.oddbox("dummy",10) == 11

    def test_box(self):
        data = numpy.ones(100)
        r,w=sm.box(data, 9,return_weights=True)
        assert numpy.all(self.test.withinAbsoluteValue(r-data,0.0,1e-10))
        assert numpy.all(self.test.withinAbsoluteValue(w,1.0/9.0,1e-10))
    
        r,w=sm.box(data, 8,return_weights=True)
        assert numpy.all(self.test.withinAbsoluteValue(r-data,0.0,1e-10))
        assert numpy.all(self.test.withinAbsoluteValue(w,1.0/9.0,1e-10))

    def test_regress_generate(self):
        """regression test of window generation"""
        
        boxsize=11
        #box
        data = numpy.ones(boxsize)
        
        regression_tests = dict(box=dict(
                                    function=sm.box,
                                    target=numpy.array([ 0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909]),
                                    args=boxsize),
                                triangle=dict(
                                    function=sm.triangle,
                                    target=numpy.array([0.01639344,  0.04918033,  0.08196721,
                                                        0.1147541 ,  0.14754098,  0.18032787,  
                                                        0.14754098,  0.1147541 ,  0.08196721,  
                                                        0.04918033,  0.01639344]),
                                    args=boxsize),
                                gaussian=dict(
                                    function=sm.gaussian,
                                    target=numpy.array([ 0.01392149,  0.03521418,  0.07247478,
                                                         0.12136501,  0.16536266,  0.18332377,
                                                         0.16536266,  0.12136501,  0.07247478,
                                                         0.03521418,  0.01392149]),
                                    args=boxsize)
                                )
        scipy_regression_tests = dict(
                                    triangle=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='triangle',
                                    target=numpy.array([ 0.02777778,  0.05555556,  0.08333333,  
                                                         0.11111111,  0.13888889,  0.16666667,  
                                                         0.13888889,  0.11111111,  0.08333333,  
                                                         0.05555556,  0.02777778]),
                                    args=boxsize),
                                    boxcar=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='boxcar',
                                    target=numpy.array([ 0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909,  0.09090909,  
                                                         0.09090909,  0.09090909]),
                                    args=boxsize),
                                    gaussian=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='gaussian',
                                    target=numpy.array([ 0.03548293,  0.05850147,  0.08630959,  
                                                         0.1139453 ,  0.13461047,  0.14230046, 
                                                         0.13461047,  0.1139453 ,  0.08630959,  
                                                         0.05850147,  0.03548293]),
                                    args=boxsize),

                                    blackman=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='blackman',
                                    target=numpy.array([ -3.30423519e-18,   9.57449104e-03,   4.78024151e-02,
                                                          1.21377890e-01,   2.02197585e-01,   2.38095238e-01,
                                                          2.02197585e-01,   1.21377890e-01,   4.78024151e-02,
                                                          9.57449104e-03,  -3.30423519e-18]),
                                    args=boxsize),

                                    parzen=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='parzen',
                                    target=numpy.array([ 0.00036423,  0.00983427,  0.04552905,  
                                                         0.12001457,  0.20305955,  0.24239665,  
                                                         0.20305955,  0.12001457,  0.04552905,  
                                                         0.00983427,  0.00036423 ]),
                                    args=boxsize),

                                    hamming=dict(
                                    function=sm.scipy_window_smooth,
                                    window_name='hamming',
                                    target=numpy.array([0.01459854,  0.03062996,  0.07260076,  
                                                        0.12447953,  0.16645033,  0.18248175,  
                                                        0.16645033,  0.12447953,  0.07260076,  
                                                        0.03062996,  0.01459854 ]),
                                    args=boxsize),

                                    )
                                
                                
        for key, value in regression_tests.items():
            r,w = value["function"](data,value["args"],return_weights=True)
            if not numpy.all(self.test.withinAbsoluteValue(w-value["target"],0.0,1e-8)):
                raise ValueError("Regression test of smoothing.{0} failed ({1})".format(key, value["function"]))
        
        import scipy
        for key, value in scipy_regression_tests.items():
            r,w = value["function"](data,value["args"],return_weights=True, window_name=value["window_name"], options=3)
            if not numpy.all(self.test.withinAbsoluteValue(w-value["target"],0.0,1e-8)):
                raise ValueError("Regression test of smoothing.{0} failed ({1})".format(key, value["function"]))
        
    