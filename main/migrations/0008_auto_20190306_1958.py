# Generated by Django 2.0 on 2019-03-06 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_stageschoolmodel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stageclassmodel',
            unique_together={('class_obj', 'comment_time')},
        ),
    ]