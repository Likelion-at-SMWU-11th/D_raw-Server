# Generated by Django 4.2.3 on 2023-08-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_guide_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('guide', 'Guide')], default='user', max_length=10),
        ),
    ]