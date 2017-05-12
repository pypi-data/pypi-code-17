def is_win32():
    import sys
    return "win32" in sys.platform


def is_linux():
    import sys
    return "linux" in sys.platform


def execute(command, callback=None):
    import subprocess
    if not is_win32():
        command = ["/bin/sh", "-c", command]
        shell = False
    else:
        shell = True
    try:
        pipe = subprocess.Popen(
            command, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        print e, command
        return e, -1

    if not callback:
        res = pipe.stdout.read()
        pipe.communicate()
        return (res, pipe.returncode)

    line = ""
    while True:
        char = pipe.stdout.read(1)
        if not char:
            break
        if char not in ["\n", "\r"]:
            line += char
            continue
        callback(line)
        line = ""
    pipe.communicate()
    return (None, pipe.returncode)
