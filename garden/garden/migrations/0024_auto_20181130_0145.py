# Generated by Django 2.0.2 on 2018-11-30 01:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0023_auto_20181128_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='uvb_end_date',
            field=models.DateField(default=datetime.date(2019, 2, 28)),
        ),
    ]