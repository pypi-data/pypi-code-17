from django import forms
from material import Layout, Row, Span2

from assetadapter import models
from assetadapter.models import Asset
from processengine.models import InputParametersEntity, DataVolume


class TaskSubjectForm(forms.ModelForm):
    layout = Layout(
        Row(Span2('id'), 'display_name'),
        Row('alias', 'address'),
        'description',
    )

    class Meta:
        model = Asset
        fields = '__all__'


class TaskParametersForm(TaskSubjectForm):
    asset = forms.ModelChoiceField(queryset=models.Asset.objects.all())

class TaskOutputForm(forms.ModelForm):

    class Meta:
        model = DataVolume
        fields = '__all__'