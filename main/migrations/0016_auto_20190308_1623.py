# Generated by Django 2.0 on 2019-03-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_classnoticemodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classnoticemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间'),
        ),
    ]