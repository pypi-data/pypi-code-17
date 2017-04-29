
class PTMLResponse:


    def __init__(this):
        this.header = {}

    def setHeader(this, name, value):
        this.header[name] = value

    def getHeaders(this):
        return this.header

# vim: set et sts=4 sw=4 :
