def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
