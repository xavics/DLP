# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dlp', '0016_transport_logistic_center'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='logistic_center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transports', to='dlp.LogisticCenter'),
        ),
    ]
