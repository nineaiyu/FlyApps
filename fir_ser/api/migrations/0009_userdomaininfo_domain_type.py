# Generated by Django 3.2.3 on 2021-09-18 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_remove_appiosdeveloperinfo_use_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdomaininfo',
            name='domain_type',
            field=models.SmallIntegerField(choices=[(0, '下载码域名'), (1, '预览下载域名')], default=1,
                                           help_text='0 表示下载码域名，扫描下载码域名，会自动跳转到预览域名', verbose_name='域名类型'),
        ),
    ]