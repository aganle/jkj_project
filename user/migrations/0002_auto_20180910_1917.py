# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-10 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64),
        ),
    ]
