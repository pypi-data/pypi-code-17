
try:
    import smart_open
    HAVE_SMART_OPEN = True
except ImportError:
    HAVE_SMART_OPEN = False


def explode_if_no_smart_open():
    if not HAVE_SMART_OPEN:
        raise ConfigurationError("s3 I/O requires the \"smart_open\" package.")
