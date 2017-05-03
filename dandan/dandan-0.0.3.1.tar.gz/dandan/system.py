def is_win32():
    import sys
    return "win32" in sys.platform


def is_linux():
    import sys
    return "linux" in sys.platform
