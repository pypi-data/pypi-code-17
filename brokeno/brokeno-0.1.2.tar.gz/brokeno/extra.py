class g:
     def __init__(self):
         self.t = 3
     def __setattr__(self, key, value):
         self.__dict__[key] = value
         print(key,value)

     def __getitem__(self, item):
         print item


a = g()




