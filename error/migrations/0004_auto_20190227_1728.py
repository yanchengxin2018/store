# Generated by Django 2.0 on 2019-02-27 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0003_auto_20190227_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errormodel',
            name='error_type',
            field=models.IntegerField(choices=[(1, '参数有错误'), (2, '服务器不能处理当前状况'), (3, '没有通过身份验证')]),
        ),
    ]