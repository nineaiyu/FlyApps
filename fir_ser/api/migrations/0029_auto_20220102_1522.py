# Generated by Django 3.2.3 on 2022-01-02 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0028_auto_20211228_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='appiosdeveloperinfo',
            name='clean_status',
            field=models.BooleanField(default=False, verbose_name='清理是否同时禁用设备ID'),
        ),
        migrations.AlterField(
            model_name='appiosdeveloperinfo',
            name='status',
            field=models.SmallIntegerField(
                choices=[(-1, '疑似被封'), (0, '未激活'), (1, '已激活'), (2, '协议待同意'), (3, '维护中'), (4, '证书过期'), (5, '状态异常')],
                default=0, verbose_name='账户状态'),
        ),
    ]
