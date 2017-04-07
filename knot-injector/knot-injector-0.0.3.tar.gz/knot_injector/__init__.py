import knot
import inspect
from functools import partial, wraps


class Container(knot.Container):

    def provide(self, name):
        return self[name]

    def add_provider(self, provider, cache, name=None):
        register_as = name or provider.__name__
        if register_as in self:
            raise AttributeError('Provider name must be unique')
        provider = self.inject(provider)
        self[register_as] = knot.FunctionCache(provider) if cache else provider

    #  decorators start
    def factory(self, **attributes):
        def register(factory):
            name = attributes.get('name', None)
            self.add_factory(factory=factory, name=name)
        return register

    def service(self, **attributes):
        def register(service):
            name = attributes.get('name', None)
            self.add_service(service=service, name=name)
        return register

    def inject(self, obj):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            @wraps(obj)
            def _wrapper(*args, **kwargs):
                return self._scan_for_injections(obj)(*args, **kwargs)
            return _wrapper
        else:
            return obj
    # decorators end

    def _scan_for_injections(self, item):
        _data = inspect.signature(item)

        _params = [
            p for p in _data.parameters
            if _data.parameters[p].default is inspect.Parameter.empty
        ]

        return self._build_partial(_params, item)

    def _build_partial(self, _params, item):
        kw = {}
        for c in _params:
            if c in self:
                if callable(self.provide(c)):
                    kw[c] = self.provide(c)(self)
                else:
                    kw[c] = self.provide(c)
        if kw:
            r = partial(item, **kw)
            r.__module__ = item.__module__
            r.__name__ = item.__name__
            return r
        return item
