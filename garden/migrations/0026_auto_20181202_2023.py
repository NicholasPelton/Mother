# Generated by Django 2.0.2 on 2018-12-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0025_auto_20181202_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='last_load',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
