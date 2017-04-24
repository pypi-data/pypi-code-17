import norns.cfg
__version__ = '0.1.0'
__author__ = "Simon van Heeringen"

def config(name=None, config_file=None, default=None):
    return norns.cfg.Config(name=name, config_file=config_file, default=default)
