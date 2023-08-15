from django import forms
from .models import Guide

class GuideCreateForm(forms.ModelForm):
    rate = forms.IntegerField(label='받은 칭찬도장 개수', initial=0)

    class Meta:
        model = Guide
        fields = '__all__'
