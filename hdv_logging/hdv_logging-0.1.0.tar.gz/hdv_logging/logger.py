import logging
import pprint
import importlib

class Handlers():
    """
    This object is container of logging handlers.
    The object will process from Logger class.
    """
    def __init__(self):
        self.handlers = {}
        
    def __setitem__(self, key, value):
        while(key in self.handlers):
            key = key + '+'
            
        self.handlers[key] = value
    pass
    
class HandlerFactory:
    """
    This factory class is most important in hdvlogging module.
    """
    def __init__(self, *args, **kargs):
        self.args = None
        self.handler_name = None
        self.level = logging.DEBUG
        self.formatter = logging.Formatter('[%(asctime)s]-%(filename)s:%(lineno)d-%(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.__init_args(args, kargs)
        handler_name = None

        if 'handler_name' in kargs:
            handler_name = kargs['handler_name']
        elif len(args):
            handler_name = args[0]
        else:
            self.add_hadler_object(logging.NullHandler())
            return
        
        if 'handlers' in kargs and isinstance(kargs['handlers'], Handlers):
            self.handlers = kargs['handlers']
            # has to delete handlers to pass logging handler object
            del kargs['handlers']
        else:
            if 'handlers' not in kargs:
                raise ValueError('handlers is minssing')
            else:
                raise TypeError('handlers has to be instance of Handlers')
            
        if 'level' in kargs:
            self.level = kargs['level']
            del kargs['level']
            
        if 'format' in kargs:
            self.formatter = logging.Formatter(kargs['format'])
            del kargs['format']
            
        self.add_handler(handler_name, self.args)
    
    def add_handler(self, handler_name, args=None):
        
        try:
            log_handlers = importlib.import_module('logging.handlers')
            handler = getattr(log_handlers, handler_name)(**args)
        except AttributeError as a:
            log_handlers = importlib.import_module('logging')
            handler = getattr(log_handlers, handler_name)(**args)
       
        handler.setLevel(self.level)
        handler.setFormatter(self.formatter)
        
        self.handlers[handler_name] = handler
    
    def add_hadler_object(self, handler):
        self.handlers.append(handler)
        
    def __init_args(self, args, kargs):
        self.args = kargs

class Logger():
    """
    Concret object to create and return logging library.
    Will unpack and apply Hanlders object from __create_loggers method 
    """
    def __init__(self, handlers=Handlers(), name='default', level=logging.DEBUG):
        
        self.handlers = handlers
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if handlers is not None and not isinstance(handlers, Handlers):
            raise TypeError('handler has to be instance of Handlers')
        
        if self.handlers.handlers == {}:
            HandlerFactory('StreamHandler', handlers=self.handlers, format='%(filename)s:%(lineno)d - %(levelname)s - %(message)s')
        
        self.__create_loggers()
        
    def __create_loggers(self):
        for h, i in self.handlers.handlers.items():
            self.logger.addHandler(i)
            
def hdvlogging(handlers=Handlers(), name='default', level=logging.DEBUG):
    """
    Helper funciton to make code little shorter 
    """
    return Logger(handlers=handlers, name=name, level=level).logger
