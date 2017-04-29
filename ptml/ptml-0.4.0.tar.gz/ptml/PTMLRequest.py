
class PTMLRequest:

    def getHeader(this, name):
        return None

    def getPathInfo(this):
        return None

    def getRequestURI(this):
        return None

    def getQueryString(this):
        return None

    def getRemoteAddress(this):
        return None

    def getRemotePort(this):
        return None

    def getRequestMethod(this):
        return None

    def hasParam(this, name):
        return None

    def getParamNames(this, name):
        return None

    def getParam(this, name):
        return None


    def has_key(this, name):
        return this.hasParam(name)

    def keys(this):
        return this.getParamNames()

    def __getitem__(this, item):
        return this.getParam(item)

# vim: set et sts=4 sw=4 :
