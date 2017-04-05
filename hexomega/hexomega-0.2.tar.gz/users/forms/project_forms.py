from ajax_select.fields import AutoCompleteSelectMultipleField
from django import forms
from django.forms import ModelForm
from users.models import AdminUser, Project


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description', 'admins']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }
        help_texts = {
            'start_date': "Please use this format: 'YYYY-MM-DD'",
            'end_date': "Please use this format: 'YYYY-MM-DD'",
            'admins': 'Hold Control to select multiple choices'
        }
