# Generated by Django 2.0 on 2019-03-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20190307_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfomodel',
            name='created_data_at',
            field=models.DateField(auto_now=True, help_text='创建日期'),
        ),
    ]
