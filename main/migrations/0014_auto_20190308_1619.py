# Generated by Django 2.0 on 2019-03-08 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_aaa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassNoticeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice', models.TextField(help_text='发布通知内容')),
                ('send_start_date', models.DateTimeField(help_text='通知的开始时间')),
                ('send_end_date', models.DateField(help_text='通知的结束时间')),
                ('class_obj', models.ForeignKey(help_text='要发布通知的班级', on_delete=django.db.models.deletion.CASCADE, to='main.ClassModel')),
            ],
        ),
        migrations.DeleteModel(
            name='AAA',
        ),
    ]
