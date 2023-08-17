from django import forms 
from .models import User, Guide

class GuideCreateForm(forms.Form):
    TERM_CHOICES = [ # 안내사 경력 기간 선택지
        ('1', '3개월 미만'),
        ('2', '3개월~6개월'),
        ('3','6개월~1년'),
        ('4', '1년 이상'),
    ]
    LOCATION_CHOICES = [ # 안내사 활동 지역 선택지
        ('1', '서울특별시'),
        ('2', '부산광역시'),
        ('3', '대구광역시'),
        ('4', '인천광역시'),
        ('5', '광주광역시'),
        ('6', '대전광역시'),
        ('7', '울산광역시'),
        ('8', '세종특별자치시'),
        ('9', '경기도'),
        ('10', '강원도'),
        ('11', '충청북도'),
        ('12', '충청남도'),
        ('13', '전라북도'),
        ('14', '전라남도'),
        ('15', '경상북도'),
        ('16', '경상남도'),
        ('17', '제주특별자치도'),
    ]
    name = forms.CharField()
    age = forms.IntegerField()
    rate = forms.IntegerField()
    start_date = forms.DateTimeField()
    career = forms.CharField()
    location = forms.CharField()

class GuideProfileEditForm(GuideCreateForm):
    class Meta:
        model = Guide
        fields = ['start_date', 'career']
