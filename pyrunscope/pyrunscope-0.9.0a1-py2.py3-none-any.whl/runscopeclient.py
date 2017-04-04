# from runscope import _import_class
#
#
# class RunScopeClient(object):
#     def __getattr__(self, item):
#         method_parts = item.split('_')
#         module = self.__module__ + '.' + method_parts[0].title() + self.resources[method_parts[1]][method_parts[0]]
#         return _import_class(module)()
