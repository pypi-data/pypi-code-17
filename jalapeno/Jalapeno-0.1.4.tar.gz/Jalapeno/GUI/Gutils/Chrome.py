

class Browse():

    def __init__(self):
        pass
    
    def __call__(self):
        from cefpython3 import cefpython as cef
        import platform
        import sys

        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize()
        cef.CreateBrowserSync(url="http://127.0.0.1:5588")
        cef.MessageLoop()
        cef.Shutdown()

Browse()()