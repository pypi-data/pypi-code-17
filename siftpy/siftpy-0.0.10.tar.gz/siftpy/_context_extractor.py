class ContextExtractor(object):
    def next(self, context_provider, context_source):
        if context_source is None:            
            raise Exception("Context source is not defined on one of your leaf nodes.")
        val = getattr(context_provider.context, context_source)
        if val is None:
            raise StopIteration()
        try:
            iterator = iter(val)            
        except:
            iterator = [val]
        for item in iterator:
            yield item

    def list(self, context_provider, context_source):
        return list(self.next(context_provider, context_source))