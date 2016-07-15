# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlp', '0011_layouts'),
    ]

    operations = [
        migrations.AddField(
            model_name='layouts',
            name='overlay_x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layouts',
            name='overlay_y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layouts',
            name='screen_x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layouts',
            name='screen_y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layouts',
            name='size_x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='layouts',
            name='size_y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]