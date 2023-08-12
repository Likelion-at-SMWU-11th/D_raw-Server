from django import forms
from .models import MatchUser

class DateInput(forms.DateInput):
    input_type='date'

class MatchBasedForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = MatchUser
        fields = '__all__'