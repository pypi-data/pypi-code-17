from evgen.core import BaseTemplate
from random import choice

class External:
    def __init__(self):
        self.Dupa = "dupa"


class MyTemplate(BaseTemplate):
    def __init__(self):
        BaseTemplate.__init__(self)
        self.External = None
        self.PrivateProp = "abc"
        self.set_attribute("static", 1)
        self.set_attribute("dynamic", self.generate_dynamic_prop)
        self.set_attribute("external", self.get_external_val)

    def add_external(self, ext):
        self.External = ext

    def get_external_val(self):
        return self.External.Dupa

    def generate_dynamic_prop(self):
        random_vals = range(5)
        return choice(random_vals)

    def basic_func(self):
        return "basic func"


mt = MyTemplate()
print mt.static
print mt.dynamic
print mt.Attributes
print mt.Attributes.get('static')
mt.update_attributes({'a':'b'})
print mt.Attributes
print mt.PrivateProp
print mt.basic_func()
mt.add_external(External())
print mt.external