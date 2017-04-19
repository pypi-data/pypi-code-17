from model import *
class OCRequestModel(OCModel):
    """docstring for OCRequestModel."""
    def __init__(self, name, secondName=None):
        OCModel.__init__(self, name, secondName)
        self.paramters=[]
    pass

    def customBuild(self):
        return self.paramters.count("custom_build") > 0

class OCServiceModel(OCRequestModel):
    def __init__(self, name, secondName=None):
        OCRequestModel.__init__(self, name, secondName)
        self.subrequests = []
    pass
