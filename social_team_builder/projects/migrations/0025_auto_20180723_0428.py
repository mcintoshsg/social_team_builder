# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_auto_20180723_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_type',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
