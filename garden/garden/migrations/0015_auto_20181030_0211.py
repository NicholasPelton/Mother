# Generated by Django 2.0.2 on 2018-10-30 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0014_outlet_water_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='uvb_end',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='outlet',
            name='uvb_start',
            field=models.IntegerField(default=6),
        ),
    ]
