"""
Author: Kit Scribe
Author email: kit.scribe@protonmail.com
Current version is 1.0.2
Solution works with a lot of colors in line without broking!
Tests are at the end of the script
"""


class WrongColor(KeyError):
    """Wrong color Error"""
    pass


class WrongStyle(KeyError):
    """Wrong style Error"""
    pass


class WrongBackground(KeyError):
    """Wrong Background Error"""
    pass


COLOR = {
    None: 0,
    'black': 30,            # it works
    'red': 31,              # it works
    'green': 32,            # it works
    'yellow': 33,           # it works
    'blue': 34,             # it works
    'magenta': 35,          # it works
    'cyan': 36,             # it works
    'gray': 37,             # it works
    }

STYLE = {
    None: 0,
    'bold': 1,              # it works
    'faint': 2,             # it might work
    'italic': 3,            # it might work
    'underline': 4,         # it works
    'blinking': 5,          # it might work
    'fast blinking': 6,     # it might work
    'reverse': 7,           # it works
    'hide': 8,              # it might work
    'strike': 9             # it might work
    }

BACKGROUND = {
    None: 0,
    'black': 40,            # it works
    'red': 41,              # it works
    'green': 42,            # it works
    'yellow': 43,           # it works
    'blue': 44,             # it works
    'magenta': 45,          # it works
    'cyan': 46,             # it works
    'gray': 47,             # it works
    }


def cprint(text, color=None, **kwargs):
    """
    Colorized print
    """
    print(colorize(text, color, **kwargs))


def colorize(text, color=None, **kwargs):
    """
    Colorize the text
    kwargs arguments:
    style=, bg=
    """
    style = None
    bg = None
    # ================ #
    # Keyword checking #
    # ================ #
    if 'style' in kwargs:
        if kwargs['style'] not in STYLE:
            raise WrongStyle('"{}" is wrong argument for {}'.format(kwargs['style'], 'style'))
        style = kwargs['style']

    if 'bg' in kwargs:
        if kwargs['bg'] not in BACKGROUND:
            raise WrongBackground('"{}" is wrong argument for {}'.format(kwargs['bg'], 'bg'))
        bg = kwargs['bg']

    if color not in COLOR:
        raise WrongColor('"{}" is wrong argument for {}'.format(color, 'color'))
    # ===================== #
    # Colorizing the string #
    # ===================== #
    if '\x1b[0m' not in text:
        text = '\x1b[' + ';'.join([str(STYLE[style]), str(COLOR[color]), str(BACKGROUND[bg])])\
               + 'm' + text + '\x1b[0m'
    else:
        lst = text.split('\x1b[0m')
        text = ''
        for x in lst:
            if not x.startswith('\x1b['):
                x = '\x1b[' + ';'.join([str(STYLE[style]), str(COLOR[color]), str(BACKGROUND[bg])])\
                     + 'm' + x + '\x1b[0m'
            else:
                x += '\x1b[0m'
            text += x
    return text
