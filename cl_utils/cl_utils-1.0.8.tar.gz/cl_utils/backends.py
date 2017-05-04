from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """
    Basically a carbon-copy of the regular ModelBackend, but verifies the user with email.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get('email')
        try:
            users = user_model.objects.filter(email__iexact=username)
            for user in users:
                if user.check_password(password):
                    return user
        except user_model.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            user_model().set_password(password)
        return None
