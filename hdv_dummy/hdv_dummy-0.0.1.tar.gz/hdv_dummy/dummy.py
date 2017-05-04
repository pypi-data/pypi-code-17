class Dummy:
    def __init__(self, *args, **kwargs):
        pass
        
    def __getattr__(self, name):
        return Dummy()
                
    def __call__(self, *args, **kwargs):
        return Dummy()