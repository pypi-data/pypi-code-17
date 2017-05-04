import nose

class Testing(object):
    def __init__(self):
        return

    def inRange(self,res, irlow,irhigh=None):
        """Returns true if res between the ranges of ir
        
        Arguments:
        res -- variable being tested, float, int, numpy array
        irlow -- lower bound
        irhigh -- upper bound
        
        Output:
        Boolean variable (possibly array) of whether irlow<=res<irhigh
        
        """
        try:
            return (res>=irlow[0])&(res<irlow[1])
        except:
            return (res>=irlow)&(res<irhigh)
    
    def withinFractionalError(self, a, b, e=None):
        """Returns true if a=b+-e
        
        Arguments:
        a -- result being tested
        b -- target value
        e -- Fraction error bars to test within against
        
        Output:
        boolean result of a=b+-e
        
        """
        if e is None:
            e=1e-4
        if (a+b) is not 0:
            return (abs((a-b)*2.0/(a+b)) < e)
        else :
            return (abs((a-b)) < e)

    def withinAbsoluteValue(self, a, b, e):
        """Returns true if a=b+-e
        
        Arguments:
        a -- result being tested
        b -- target value
        e -- error bars to test within against
        
        Output:
        boolean result of a=b+-e
        
        """
        return self.inRange(a,b-e,b+e)
    
    def debug(self, funcname):
        """Prints a nice message 
        
        Arguments:
        functname -- name of test function that called debug
        
        """
        print("Testing...{0}".format(funcname))

    
    def test_inRange(self):
        self.debug("inRange")
        assert(self.inRange(1.0,0.0,2.0))
        assert(self.inRange(1.1,1.09,1.11))
        assert(not self.inRange(0.0,1.09,1.11))

    def test_withinAV(self):
        self.debug("withinAV")
        assert(self.withinAbsoluteValue(0.0,0.0,1e-4))
        assert(self.withinAbsoluteValue(0.0,1e-5,1e-4))
        assert(not self.withinAbsoluteValue(0.0,1.0,0.99))
        
    def test_withinFR(self):
        self.debug("withinFR")
        assert(self.withinFractionalError(1.0,1.0,1e-4))
        assert(self.withinFractionalError(1.0,1.01,0.1))
        assert(self.withinFractionalError(1.0,1.01,0.01))
        assert(not self.withinFractionalError(1.0,1.01,0.009))
        assert(not self.withinFractionalError(0.0,1.0,1e-3))
        assert(not self.withinFractionalError(0.0,1.0,1e-3))

    def test_testing(self):
        assert True
        assert not False
        self.test_inRange()
        self.test_withinAV()
        self.test_withinFR()


if __name__=="__main__":
    t=Testing()
    t.test_testing()
