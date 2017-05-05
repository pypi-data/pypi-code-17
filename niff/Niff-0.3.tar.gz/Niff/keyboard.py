import sys
import termios
import contextlib


@contextlib.contextmanager
def on_keyboard_ready():
    file = sys.stdin
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)




def on_keyboard():
    with on_keyboard_ready():
        while 1:
            ch = got_key()

            if not ch or ch == chr(4):
                break

            yield ch



if __name__ == '__main__':
    main()