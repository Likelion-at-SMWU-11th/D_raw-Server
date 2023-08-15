from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Guide(models.Model):
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
    name = models.CharField(verbose_name='안내사 이름', max_length=5, null=True, default='')
    age = models.IntegerField(verbose_name='나이', null=True, default=0)
    rate = models.IntegerField(verbose_name='받은 칭찬도장 개수', null=True)
    start_date = models.DateTimeField(verbose_name='안내사 첫 시작일', null=True)
    career = models.CharField(verbose_name='안내사 경력', choices=TERM_CHOICES, max_length=20, null=True, default='')
    location = models.CharField(verbose_name='안내사 활동 가능 지역', choices=LOCATION_CHOICES, max_length=20, null=True, default='')\
    
class User(models.Model):
    pass