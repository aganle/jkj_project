# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-11 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitem_isdelete'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItemManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='isDelete',
            new_name='isdelete',
        ),
    ]
