from django import forms
from .models import Guide, GuideLocation

class GuideCreateForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = '__all__'

class GuideLocationForm(forms.ModelForm):
    class Meta:
        model = GuideLocation
        fields = '__all__'