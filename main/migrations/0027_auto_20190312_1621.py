# Generated by Django 2.0 on 2019-03-12 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20190312_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentinfomodel',
            old_name='degree',
            new_name='degree_name',
        ),
    ]