# Generated by Django 2.0 on 2019-03-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0009_auto_20190307_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='cookie_data',
            field=models.BinaryField(help_text='被转化为文本的cookie的数据', null=True),
        ),
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='exception_data',
            field=models.BinaryField(help_text='记录异常的提示信息', null=True),
        ),
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='get_data',
            field=models.BinaryField(help_text='被转化为文本的get的数据', null=True),
        ),
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='header_data',
            field=models.BinaryField(help_text='被转化为文本的header的数据', null=True),
        ),
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='post_data',
            field=models.BinaryField(help_text='被转化为文本的post的数据', null=True),
        ),
        migrations.AlterField(
            model_name='exceptionlogmodel',
            name='url',
            field=models.TextField(help_text='原始的访问URL', null=True),
        ),
    ]
