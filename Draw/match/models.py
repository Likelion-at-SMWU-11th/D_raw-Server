from django.db import models
from django import forms

class MatchUser(models.Model):
    date = models.DateField(verbose_name='date', auto_now_add=True)
    start_time = models.DateTimeField(verbose_name='start_time', auto_now_add=True)
    finish_time = models.DateTimeField(verbose_name='finish_time', auto_now_add=True)
    
    # 장소
    place = models.TextField(verbose_name='place')

    # 시각장애 여부
    BLIND_CHOICES = [
        ('L', '없음'),
        ('M', '경증 장애'),
        ('H', '중증 장애'),
    ]
    blind = models.CharField(
        choices=BLIND_CHOICES, max_length=3, null='없음'
    )

    # 출생년도 선택 리스트
    birth = models.PositiveIntegerField(
        verbose_name='Birth',
        choices=[(year, year) for year in range(1905, 2005)],
    )

    # 성별 선택 리스트
    GENDER_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
    ]
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=2, blank=True
    )

class PreferUser(models.Model):
    # 선호하는 성별
    GENDER_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
        ("N", "모두 가능"),
    ]
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=3, blank=True
    )

    # 집중 케어 필요 항목
    LIST_CHOICES = [
        ("Bank", "모바일 뱅킹"),
        ("Ecommerce", "전자상거래"),
        ("Service", "공공서비스"),
        ("Docs", "전자 문서 처리"),
        ("Sns", "소셜 미디어"),
        ("Kiosk", "키오스크"),
    ]

    list = models.CharField(
        choices=LIST_CHOICES, max_length=9
    )

    # 안내사 매칭 추가 문의
    PLUS_CHOICES = [
        ("Y", "성인 안내사 선호"),
        ("N", "연령 상관 없음"),
    ]

    plus = models.CharField(
        choices=PLUS_CHOICES, max_length=2
    )

    # 그 외 유의사항
    care = models.CharField(max_length=300, null=True)