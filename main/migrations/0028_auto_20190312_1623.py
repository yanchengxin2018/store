# Generated by Django 2.0 on 2019-03-12 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20190312_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentinfomodel',
            old_name='class_name',
            new_name='class_name_log',
        ),
        migrations.RenameField(
            model_name='studentinfomodel',
            old_name='degree_name',
            new_name='degree_name_log',
        ),
        migrations.RenameField(
            model_name='studentinfomodel',
            old_name='study_time',
            new_name='study_time_log',
        ),
    ]