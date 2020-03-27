# Generated by Django 3.0.3 on 2020-03-27 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20200326_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appstorage',
            name='additionalparameters',
            field=models.TextField(blank=True, help_text='阿里云:{"sts_role_arn":"arn信息","endpoint":""}  七牛云:{"domain_name":""} 本地存储:{"domain_name":""}', max_length=256, null=True, verbose_name='额外参数'),
        ),
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='关联用户'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='账户状态，默认启用'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='storage',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_storage', to='api.AppStorage', verbose_name='存储'),
        ),
    ]