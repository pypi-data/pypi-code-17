from django import forms
from django.contrib.admin.widgets import AdminDateWidget, FilteredSelectMultiple, AdminSplitDateTime
from django.forms import ModelForm

from users.models import MemberUser, Task


class CreateTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        ms = MemberUser.objects.filter(project__name=self.data.get('pn'))
        c = [(m.id, m.get_full_name()) for m in ms]
        self.fields['members'].choices = c
        self.fields['members'].required = False
        self.fields['title'].required = True

    class Meta:
        model = Task
        fields = ['title', 'status', 'est_end', 'to_leader', 'members']

        widgets = {
            # 'est_end': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'est_end': AdminDateWidget(),
            'members': forms.CheckboxSelectMultiple()
        }
        help_texts = {
            'est_end': "Please use this format: 'YYYY-MM-DD'",
            'users': 'Hold down Control/Cmd to select more than member for the task.'
        }

    def clean(self):
        print('United Abominations')
        cleaned_data = super(ModelForm, self).clean()
        return cleaned_data


class LeaderUpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'status', 'est_end', 'description', 'deliverable', 'to_leader', 'members']

        widgets = {
            'est_end': AdminDateWidget(),
            'members': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        pn = kwargs.pop('pn')
        up_flag = kwargs.pop('up_flag')
        up_name = kwargs.pop('up_name')
        qs = MemberUser.objects.filter(project__name=pn)
        c = [(m.id, m.get_full_name()) for m in qs]
        super(LeaderUpdateTaskForm, self).__init__(*args, **kwargs)
        self.fields['members'].choices = c
        self.fields['members'].required = False
        self.fields['title'].required = True
        if up_flag:
            self.fields.pop('deliverable')
            self.fields['Deliverable'] = forms.CharField(max_length=50, required=False)
            self.fields['Deliverable'].initial = "Deliverable [{}] already uploaded.".format(up_name)
            self.fields['Deliverable'].widget.attrs['readonly'] = True

            self.fields['title'].widget.attrs['readonly'] = True

            self.initial['status'] = 'Completed'
            self.fields['status'] = forms.CharField(max_length=50, required=False)
            self.fields['status'].widget.attrs['readonly'] = True

            self.fields['est_end'] = forms.CharField(max_length=50, required=False)
            self.fields['est_end'].widget.attrs['readonly'] = True

            self.fields['description'] = forms.CharField(max_length=50, required=False)
            self.fields['description'].widget.attrs['readonly'] = True

            self.fields['to_leader'] = forms.CharField(max_length=50, required=False)
            self.fields['to_leader'].widget.attrs['readonly'] = True

            self.fields['members'] = forms.CharField(max_length=50, required=False)
            names = ''
            for m in self.initial['members']:
                names += m.get_full_name()
                names += ', '
            self.initial['members'] = names[:-2]
            self.fields['members'].widget.attrs['readonly'] = True
