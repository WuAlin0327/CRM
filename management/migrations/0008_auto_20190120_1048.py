# Generated by Django 2.1.4 on 2019-01-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_auto_20190120_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.IntegerField(null=True, verbose_name='电话号码'),
        ),
    ]
