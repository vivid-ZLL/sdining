# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-22 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_businesstextcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='total_rank',
            field=models.IntegerField(default=0, verbose_name='总分'),
        ),
    ]
