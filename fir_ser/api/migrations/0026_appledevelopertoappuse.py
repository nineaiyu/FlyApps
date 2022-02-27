# Generated by Django 3.2.3 on 2021-12-13 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0025_delete_devicequeue'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppleDeveloperToAppUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usable_number', models.IntegerField(default=100, verbose_name='可使用设备数')),
                ('description', models.CharField(blank=True, default='', max_length=256, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.apps')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.appiosdeveloperinfo')),
            ],
            options={
                'verbose_name': '开发者专属于应用',
                'verbose_name_plural': '开发者专属于应用',
                'unique_together': {('app_id', 'developerid')},
            },
        ),
    ]