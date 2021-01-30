# Generated by Django 3.0.3 on 2021-01-27 21:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0011_auto_20210125_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='udidsyncdeveloper',
            name='platform',
            field=models.SmallIntegerField(choices=[(0, 'fly分发'), (1, 'app developer')], default=0,
                                           verbose_name='udid所在平台'),
        ),
    ]