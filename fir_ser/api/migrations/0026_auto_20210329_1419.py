# Generated by Django 3.0.3 on 2021-03-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0025_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.BigIntegerField(verbose_name='下载包价格'),
        ),
    ]