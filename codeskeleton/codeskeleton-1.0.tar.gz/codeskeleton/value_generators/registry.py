class ValueGeneratorRegistry(object):
    """
    Registry of generators for
    :class:`codeskeleton.spec.variable.Variable`.
    """
    def __init__(self):
        self.generators = {}

    def register(self, generator_name, function):
        """
        Register a generator function.

        Args:
            generator_name (str): The name of the generator.
            function: The generator function. The generator function
                must return a generated value.
        """
        self.generators[generator_name] = function

    def generate_value(self, generator_name, **kwargs):
        """
        Generate a value.

        Args:
            generator_name (str): Name of the generator to execute.
            **kwargs: Kwargs for the generator function..
        """
        return self.generators[generator_name](**kwargs)

    def __contains__(self, generator_name):
        return generator_name in self.generators

    def namelist(self):
        return list(self.generators.keys())


#: The generator registry. Use this to access the generator registry
#: (do not create a new :class:`.ValueGeneratorRegistry` object.
GENERATOR_REGISTRY = ValueGeneratorRegistry()
