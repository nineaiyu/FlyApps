# Generated by Django 3.0.3 on 2021-03-08 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0019_auto_20210308_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='new_bundle_id',
            field=models.CharField(blank=True, help_text='用与超级签某些因素下修改包名', max_length=64, null=True,
                                   verbose_name='new_bundle_id'),
        ),
    ]
