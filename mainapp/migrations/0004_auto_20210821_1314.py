# Generated by Django 3.1 on 2021-08-21 05:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210821_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='music',
            name='last_modify_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
