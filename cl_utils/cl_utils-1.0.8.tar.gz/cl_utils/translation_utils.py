from django.utils import translation


def language(lang):
    """
    Execute the content of this block in the language of the user.
    To be used as follows:

    with language(lang):
       some_thing_in_this_language()

    """
    class with_block(object):
        def __enter__(self):
            self._old_language = translation.get_language()
            translation.activate(lang)

        def __exit__(self, *args):
            translation.activate(self._old_language)

    return with_block()



def user_language(user):
    """
    Execute the content of this block in the language of the user.
    To be used as follows:

    with user_language(user_obj):
       some_thing_to_do_in_his_language()

    """
    return language(user.get_profile().language)

