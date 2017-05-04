from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username or email"), max_length=75)
