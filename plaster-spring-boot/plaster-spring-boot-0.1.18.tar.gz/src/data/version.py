import pkg_resources

# As defined in setup.py
__version__ = pkg_resources.require("plaster-spring-boot")[0].version
