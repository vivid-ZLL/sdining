# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-19 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20170819_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_comment',
            field=models.BooleanField(default=False, verbose_name='是否评价'),
        ),
    ]
