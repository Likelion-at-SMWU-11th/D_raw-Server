# Generated by Django 4.2.3 on 2023-08-14 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_guidelocation_remove_guide_rate_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GuideLocation',
        ),
        migrations.AddField(
            model_name='guide',
            name='location',
            field=models.CharField(choices=[('1', '서울특별시'), ('2', '부산광역시'), ('3', '대구광역시'), ('4', '인천광역시'), ('5', '광주광역시'), ('6', '대전광역시'), ('7', '울산광역시'), ('8', '세종특별자치시'), ('9', '경기도'), ('10', '강원도'), ('11', '충청북도'), ('12', '충청남도'), ('13', '전라북도'), ('14', '전라남도'), ('15', '경상북도'), ('16', '경상남도'), ('17', '제주특별자치도')], default='', max_length=20, null=True, verbose_name='안내사 활동 가능 지역'),
        ),
        migrations.AddField(
            model_name='guide',
            name='rate',
            field=models.IntegerField(default=0, null=True, verbose_name='받은 칭찬도장 개수'),
        ),
        migrations.AddField(
            model_name='guide',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='안내사 첫 시작일'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='age',
            field=models.IntegerField(default='', null=True, verbose_name='나이'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='career',
            field=models.CharField(choices=[('1', '3개월 미만'), ('2', '3개월~6개월'), ('3', '6개월~1년'), ('4', '1년 이상')], default='', max_length=20, null=True, verbose_name='안내사 경력'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='name',
            field=models.CharField(default='', max_length=5, null=True, verbose_name='안내사 이름'),
        ),
    ]
