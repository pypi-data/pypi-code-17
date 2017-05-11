import nose.tools
from dwell.caselessdict import CaselessDict
from dwell.testing import Testing

class test_CaselessDict(object):
    def __init__(self):
        self.test = Testing()
        return
    
    def test_null(self):
        self.test.debug("null")
        assert(True)
        
    def test_init(self):
        self.test.debug("empty init")
        a=CaselessDict()
        self.test.debug("copy init1")
        a=CaselessDict({"a":1,"b":2})
        self.test.debug("copy init2")
        a=CaselessDict({"a":1,"A":2})

    def test_getset(self):
        a=CaselessDict()
        self.test.debug("set")
        a["a"]=1
        self.test.debug("get")
        b=a["a"]
        assert(b==a["a"])
        self.test.debug("contains")
        assert("a" in a)
        assert(not "b" in a)
        
        self.test.debug("get2")
        assert(a.get("b",2)==2)
        assert(not a.get("b",3)==2)
        self.test.debug("setdefault")
        assert(a.setdefault("c",3)==3)
        
    def test_addondict(self):
        self.test.debug("update")
        a=CaselessDict()
        a.update({"a":1,"b":2})
        assert("a" in a and "b" in a)
        a.update(CaselessDict({"A":2,"c":3}))
        assert("c" in a and "b" in a and "a" in a)
        assert(a["a"]==a["A"])
        self.test.debug("init")
        b=CaselessDict(zip(["a","b","A"],[1,2,3]))
        assert(b["a"]==b["A"])
        assert(b["a"]==3)
        assert(len(b.keys())==2)
        #test pop

        self.test.debug("pop")
        q=b.pop("a")
        assert(q==3)
        assert(len(b.keys())==1)
        assert(b["b"]==2)
        #test pop with different case
        b["a"]=2
        assert(len(b.keys())==2)
        b.pop("A")
        assert(len(b.keys())==1)
        #test pop with invalid key
        b["a"]=2
        assert(len(b.keys())==2)
        try:
            b.pop("q")
            assert(False)
        except:
            assert(True)
        assert(len(b.keys())==2)

    def test_copy(self):
        self.test.debug("copy")
        a=CaselessDict({"a":1,"b":2})
        b=a.copy()
        assert(a==b)
        assert(a["a"]==b["a"])
        assert(a["a"]!=b["b"])
        assert(a["b"]==b["b"])

    def test_case(self):
        self.test.debug("case match")
        a=CaselessDict({"a":1,"A":2,"b":3})
        assert(a["a"]==a["A"])
        assert(a["a"]==2)
        assert(a["A"]==2)
        assert(not a["b"] == 2)
        assert(not a["b"] == a["a"])


        
    def alltest(self):
        self.test_null()
        self.test_init()
        self.test_case()
        self.test_getset()
        self.test_addondict()
        self.test_copy()
        pass
    
    
    
if __name__ == "__main__":
    t=test_CaselessDict()
    t.alltest()
        
