# Generated by Django 3.0.3 on 2021-04-18 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0041_auto_20210416_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='支付商家名称'),
        ),
    ]
