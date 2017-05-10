# -*- coding: utf-8 -*-
from .http import HTTP
from .config import open_apis


class APIMixin(HTTP):

    def __init__(self):
        self.api_method = ""

    def __getattr__(self, name):
        if not hasattr(super(), name):
            self.set_attr(name)
        return self.__getattribute__(name)

    def set_attr(self, name):
        if name in open_apis:
            super().__setattr__(name, self.attr_func)
            self.api_method = name
        else:
            raise AttributeError(
                "\n-----------------------------------------------------\n"
                "The API method \'%s\' is not supported by Everysense."
                "\n-----------------------------------------------------\n"
                "Surpported API methods are: "
                "%s" 
                "\n-----------------------------------------------------\n"
                % (str(name), str(open_apis))
                )
                
    def attr_func(self, kwargs):
        return self.request(self.api_method, kwargs)
