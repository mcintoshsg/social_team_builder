# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-07 02:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0026_auto_20180723_0815'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='position',
            unique_together=set([('project', 'skill')]),
        ),
    ]