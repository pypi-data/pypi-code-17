from django.test import TestCase
from django.conf import settings

from django import forms


class MyForm(forms.Form):
    required_field = forms.CharField(required=True)
    optional_field = forms.CharField(required=False)
    colours = forms.MultipleChoiceField(
        choices=(("blue", "Blue"), ("red", "Red")),
        widget=forms.widgets.CheckboxSelectMultiple,
        required=False
    )
    some_date = forms.DateTimeField(
        widget=forms.widgets.SplitDateTimeWidget,
        required=False
    )
    a_colour = forms.ChoiceField(
        choices=(("blue", "Blue"), ("red", "Red")),
        widget=forms.widgets.RadioSelect,
        required=False
    )


class FormTestCase(TestCase):

    def test_required_attr(self):
        """Only one field gets the required attribute"""
        form = MyForm()
        li = form.as_p().split("required=\"required\"")
        self.assertEqual(len(li), 2)

    def test_as_div(self):
        form = MyForm()
        self.failUnless("<div class=\" Form-item Field" in form.as_div())

    def test_as_some_renderer(self):
        form = MyForm()
        self.failUnless("<div class=\"field\">" in form.as_some_renderer())
