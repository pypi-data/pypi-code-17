from django import forms
from users.models import LeaderUser


class LeaderForm(forms.Form):
    username = forms.CharField(label='Username', max_length=8, min_length=8)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email')

    def clean_email(self):
        data = self.cleaned_data['email']
        if LeaderUser.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    class Meta:
        model = LeaderUser


class UpdateLeaderForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea)

    def clean_email(self):
        data = self.cleaned_data['email']
        if self.has_changed() is False:
            if LeaderUser.objects.filter(email=data).exists():
                raise forms.ValidationError("This email already used")
            return data
        else:
            return data

    class Meta:
        model = LeaderUser
