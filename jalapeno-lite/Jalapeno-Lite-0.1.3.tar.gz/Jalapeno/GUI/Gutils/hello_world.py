# Hello world example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v55.3+.
# from cefpython3 import cefpython as cef
# import platform
# import sys
from multiprocessing import Process
import time
class runner(Process):

    def __init__(self):

        Process.__init__(self)
    @staticmethod
    def run():
        from cefpython3 import cefpython as cef
        import platform
        import sys

        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize()
        cef.CreateBrowserSync(url="https://www.google.com/")
        cef.MessageLoop()
        cef.Shutdown()


if __name__ == '__main__':


    runner().run()
