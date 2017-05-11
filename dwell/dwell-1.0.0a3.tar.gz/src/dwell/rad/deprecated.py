"""Module to generate deprecation warnings for functions that are no longer used.
To use this package, import it (`from dwell.RAD.deprecated import deprecated`) and
wrap a deprecated function with @deprecated.
Optional arguments include a nicer message (for wrapping class methods, say) in `message`,
a `replacement` function, and a requirement to `use_replacement` instead of the called
function _with the same arguments_
"""
#This module is BSD licensed

license="BSD"
import warnings
import dwell.rad.terminal as t
warnings.simplefilter("always")

class _deprecated(object):
    """deprecated class"""
    def __init__(self, function, message=None, replacement=None, use_replacement=False):
        """Initialize deprecation message. This initialization takes the `function`
        to be deprecated, an optional nice `message`, a possible `replacement` function,
        and an instruction to `use_replacement` instad of the old function."""

        self.function = function
        self.message = message
        self.replacement = replacement
        self.use_replacement = use_replacement
        self.__name__ = self.function.__name__
        self.__doc__ = self.function.__doc__
        self.__dict__.update(self.function.__dict__)

    def __call__(self,*args,**kwargs):
        """Wrapper to function() so that you can call this class as if it were
        a function"""
        #build the message
        if self.message is None:
            message = "{0} is deprecated.".format(self.function.__name__)
        else:
            message = self.message
        #notify of a replacement
        if self.replacement is not None:
                message += " use {0} instead".format(self.replacement.__name__)
        #warn the user, in magenta.
        warnings.warn(t.warning(message), DeprecationWarning, stacklevel=2)

        #call the function, or replacement
        try:
            if self.use_replacement:
                return self.replacement(*args, **kwargs)
            else:
                return self.function(*args, **kwargs)
        except TypeError as e:
            if self.use_replacement:
                return self.replacement()
            else:
                return self.function()

def deprecated(function=None, message=None, replacement=None, use_replacement=False):
    """Wrapper function that deals with the possibility of keyword arguments that
    results in the default argument (the function) being None. In this case, a closure
    function is generated (wrapper) that stores the keyword arguments and returns
    a new wrapper function (which then wraps the function being deprecated, but with
    hidden arguments)."""
    if function:
        return _deprecated(function)
    else:
        def wrapper(function):
            return _deprecated(function, message, replacement, use_replacement)
        return wrapper
