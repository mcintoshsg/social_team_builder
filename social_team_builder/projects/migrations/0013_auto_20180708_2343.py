# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-08 23:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20180707_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='role',
            new_name='skill',
        ),
    ]