# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 20:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlp', '0004_auto_20160610_1858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='droppoint',
            old_name='altitude',
            new_name='alt',
        ),
        migrations.RenameField(
            model_name='droppoint',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='droppoint',
            old_name='longitude',
            new_name='lng',
        ),
        migrations.RenameField(
            model_name='logisticcenter',
            old_name='altitude',
            new_name='alt',
        ),
        migrations.RenameField(
            model_name='logisticcenter',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='logisticcenter',
            old_name='longitude',
            new_name='lng',
        ),
    ]
