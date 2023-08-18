from django import forms
from .models import MatchUser

class DateInput(forms.DateInput):
    input_type = 'date'

class Choice(forms.ModelForm):
    class Meta:
        model = MatchUser
        fields = ['method']

class MatchBasedForm(forms.ModelForm):
    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=MatchUser.LIST_CHOICES,
    )
    
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = MatchUser
        fields = ['time_choice', 'start_hour', 'place',
                  'blind', 'birth', 'gender', 'prefer_gender',
                  'plus', 'care']