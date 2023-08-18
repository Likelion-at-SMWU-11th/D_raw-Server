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
    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'age', 'rate', 'career', 'location']

class GuideProfileEditForm(GuideCreateForm):
    class Meta:
        model = User
        fields = ['start_date', 'career']

class GuideProfileCreationForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'gender', 'age', 'location']

    username = forms.CharField(max_length=10)
    gender_type = forms.ChoiceField(choices= [('1', '남성'), ('2', '여성')])
    age_type = forms.ChoiceField(choices = [('1', '2003년'), ('2', '2002년'), ('3', '2001년'), ('4', '2000년'), ('5', '1999년'), ('6', '1998년'), ('7', '1997년'), ('8', '1996년'), ('9', '1995년'), ('10', '1994년'), ('11', '1993년'), ('12', '1992년')])
    location_type = forms.ChoiceField(choices = [
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
    ])
        
class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(choices=[('guide', 'Guide'), ('user', 'User')])


class GuideCareerForm(forms.Form):
    career_type = forms.ChoiceField(choices=[('1', '3개월 미만'), ('2', '3개월~6개월'), ('3', '6개월~1년'), ('4', '1년 이상')])