# Generated by Django 2.0 on 2019-03-06 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_studentinfomodel_edit_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='StageClassModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_time', models.DateField(help_text='提交一个时间,在这天时,这个班级的老师会被要求提交阶段性评价')),
                ('class_obj', models.ForeignKey(help_text='当comment_time这个时间点到达,这个班级的老师会被要求提交阶段性评价', on_delete=django.db.models.deletion.CASCADE, to='main.ClassModel')),
            ],
        ),
    ]
