from django import forms
from users.models import AdminUser, User


class AdminUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=8, min_length=8)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    bio = forms.CharField(label='Bio', widget=forms.Textarea, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AdminUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username exists in the system.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AdminUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists in the system.")
        return email

    class Meta:
        model = AdminUser


class AdminUpdateForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea, required=False)

    class Meta:
        model = AdminUser

    def clean_email(self):
        if 'email' in self.changed_data:
            if AdminUser.objects.filter(email=self.cleaned_data.get('email')).exists():
                raise forms.ValidationError("Email exists in the system.")
            print('changed!')
        else:
            print('no!')
        return self.cleaned_data.get('email')


class UserUpdateForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6, required=False)

    def clean_email(self):
        if 'email' in self.changed_data:
            if User.objects.filter(email=self.cleaned_data.get('email')).exists():
                raise forms.ValidationError("Email exists in the system.")
            print('changed!')
        else:
            print('no!')
        return self.cleaned_data.get('email')
