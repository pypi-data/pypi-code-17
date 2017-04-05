from django import forms
from users.models import AdminUser


class AdminUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea)

    class Meta:
        model = AdminUser


# It was I, It was needed. Change is inevitable.
class AdminUpdateForm(forms.Form):
    # username = forms.CharField(label='Username', max_length=10)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea)

    class Meta:
        model = AdminUser


class PasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)
