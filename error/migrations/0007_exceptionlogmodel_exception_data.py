# Generated by Django 2.0 on 2019-03-07 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0006_auto_20190307_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceptionlogmodel',
            name='exception_data',
            field=models.TextField(default=1, help_text='记录异常的提示信息'),
            preserve_default=False,
        ),
    ]