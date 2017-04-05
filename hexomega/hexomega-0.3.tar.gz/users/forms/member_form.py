from django import forms

from users.models import MemberUser


class MemberUpdate(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=50, widget=forms.EmailInput, required=False)
    password = forms.CharField(max_length=30, min_length=8, widget=forms.PasswordInput, required=False, initial=' ')
    phone = forms.CharField(max_length=15, show_hidden_initial='+651234578', required=False)


class MemberCreate(forms.ModelForm):
    username = forms.CharField(max_length=8, min_length=8, required=True,
                               help_text='Username should contain exactly 8 characters. (Murdoch ID)')

    class Meta:
        model = MemberUser
        fields = ['username', 'first_name', 'last_name', 'role', 'email', 'phone']
