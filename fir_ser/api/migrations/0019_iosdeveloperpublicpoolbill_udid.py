# Generated by Django 3.2.3 on 2021-11-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0018_devicequeue'),
    ]

    operations = [
        migrations.AddField(
            model_name='iosdeveloperpublicpoolbill',
            name='udid',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='设备udid'),
        ),
    ]