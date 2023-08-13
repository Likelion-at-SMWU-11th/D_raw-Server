from django.db import models

class Guide(models.Model):
    name = models.CharField(verbose_name='안내사 이름', max_length=5)
    age = models.IntegerField(verbose_name='나이')
    rate = models.IntegerField(verbose_name='받은 칭찬도장 개수')
    start_date = models.DateTimeField(verbose_name='안내사 첫 시작일')
    career = models.IntegerField()