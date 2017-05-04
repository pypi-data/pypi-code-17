"""Terminal prompt utilities"""
import six
# prompt
def prompt(text=None, choices=None, default=None):
    """Create a prompt of text is given,then offer choices with a default.
    e.g. prompt('how are you?',['good','bad'],['good']"""

    if text is None:
        text = ""

    use_choices = None
    if choices is not None:
        if type(choices) is list:
            use_choices = dict(zip(choices, choices))
        elif type(choices) is dict:
            use_choices = choices

    while True:
        if use_choices is None:
            ans = six.input("{text}: ".format(text=text))
            if not ans:
                return default
            else:
                return ans

        else:  # choices
            ans = six.input("{text} [{choices}]: ".format(text=text,
                                                    choices=",".join(
                                                    use_choices.keys())))
            for k in use_choices.keys():
                if (type(use_choices[k]) == str and ans == use_choices[k]) or\
                (type(use_choices[k]) == list and ans in use_choices[k]):
                    return k
            #no choice found
            if default is not None:
                return default

            message("Please enter one of the choices.")
            continue


def yesno(text=None):
    """Wrapper around prompt for a simple yes/no question"""
    choices = {"y": ["YES", "yes", "y", "Y"],
               "n": ["NO", "no", "n", "N"]}

    res = {"y": True, "n": False}
    return res[prompt(text, choices=choices, default=None)]
