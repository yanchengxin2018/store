# Generated by Django 2.0 on 2019-03-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20190311_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfomodel',
            name='degree',
            field=models.CharField(help_text='记录这条信息时,学生的课程章节', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='studentinfomodel',
            name='study_time',
            field=models.DateTimeField(null=True),
        ),
    ]