'''
 * Set value true to print logs.
 * for Production environment, set as false.
 '''
LOG_ENABLED = False


class Logger(object):
    """docstring for Logger"""

    @staticmethod
    def logInfo(string):
        if LOG_ENABLED:
            print(string)

    @staticmethod
    def logError(errorObj):
        Logger.dumpObject(errorObj)

    @staticmethod
    def printResponsePacket(obj):
        if LOG_ENABLED:
            print(obj.url)
            print(obj.text)
            print(obj.status_code)
            obj.close()

    @staticmethod
    def dumpObject(obj):
        if LOG_ENABLED:
            for attr in dir(obj):
                if hasattr(obj, attr):
                    print("%s = %s" % (attr, getattr(obj, attr)))
