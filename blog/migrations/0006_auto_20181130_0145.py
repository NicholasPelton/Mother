# Generated by Django 2.0.2 on 2018-11-30 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20181128_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='comments',
            field=models.TextField(default='Hello I am commenting!'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
