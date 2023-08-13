from django import forms
from .models import Guide

class GuideForm(forms.Form):
    TERM_CHOICES = [ # 안내사 경력 기간 선택지
        ('1', '3개월 미만'),
        ('2', '3개월~6개월'),
        ('3','6개월~1년'),
        ('4', '1년 이상'),
    ]
    name = forms.CharField(label='안내사 이름', max_length=10) # 안내사 이름
    age = forms.IntegerField(label='나이') # 안내사 나이
    rate = forms.IntegerField(label='받은 칭찬도장 개수') # 안내사 받은 도장 개수
    career = forms.ChoiceField(label='안내사 경력', choices=TERM_CHOICES) # 안내사 경력
    start_date = forms.DateTimeField(label='안내사 첫 활동일') # 안내사 첫 활동일

class GuideCreateForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = '__all__'