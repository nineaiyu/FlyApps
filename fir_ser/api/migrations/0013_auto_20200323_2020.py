# Generated by Django 3.0.3 on 2020-03-23 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_userinfo_head_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreleaseinfo',
            name='is_master',
            field=models.BooleanField(default=True, verbose_name='是否master版本'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='head_img',
            field=models.CharField(default='/files/imgs/head_img.jpeg', max_length=256, verbose_name='个人头像'),
        ),
        migrations.CreateModel(
            name='AppStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='存储名字')),
                ('storage_type', models.SmallIntegerField(choices=[(0, '本地存储'), (1, '七牛云存储'), (2, '阿里云存储'), (3, '默认存储')], default=3, verbose_name='存储类型')),
                ('access_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问key')),
                ('secret_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问secret')),
                ('bucket_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储空间bucket_name')),
                ('additionalparameters', models.TextField(blank=True, help_text='阿里云:{"sts_role_arn":"arn信息","endpoint":""}  七牛云:{"domain_name":""}', max_length=256, null=True, verbose_name='额外参数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '存储配置',
                'verbose_name_plural': '存储配置',
            },
        ),
    ]
