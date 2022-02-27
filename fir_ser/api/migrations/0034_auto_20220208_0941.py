# Generated by Django 3.2.3 on 2022-02-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0033_appiosdeveloperinfo_auto_check'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appudid',
            name='is_download',
        ),
        migrations.RemoveField(
            model_name='appudid',
            name='is_signed',
        ),
        migrations.AddField(
            model_name='apps',
            name='change_auto_sign',
            field=models.BooleanField(default=False, verbose_name='签名相关的数据更新自动签名'),
        ),
        migrations.AddField(
            model_name='appudid',
            name='sign_status',
            field=models.SmallIntegerField(
                choices=[(0, '新设备入库准备'), (1, '设备ID已经注册'), (2, 'bundelid已经注册'), (3, '描述文件已经下载'), (4, '已经完成签名打包')],
                default=0, verbose_name='签名状态'),
        ),
    ]