# Generated by Django 2.0.2 on 2018-11-28 22:46

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0023_auto_20181128_2246'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('photo', models.ImageField(upload_to=blog.models.upload_to)),
                ('temp_high', models.DateField(default=0)),
                ('temp_low', models.DateField(default=0)),
                ('humidity_high', models.DateField(default=0)),
                ('humidity_low', models.DateField(default=0)),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.Garden')),
            ],
        ),
        migrations.RemoveField(
            model_name='log',
            name='garden',
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
