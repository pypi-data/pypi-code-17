def actually_bytes(stringy):
    if type(stringy) == str:
        pass
    elif type(stringy) != unicode:
        stringy = str(stringy)
    if type(stringy) == unicode:
        stringy = stringy.encode("utf-8")
    return stringy