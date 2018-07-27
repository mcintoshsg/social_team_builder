# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20180722_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill', to='projects.Skill'),
        ),
    ]