# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-13 20:03
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0010_auto_20171013_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='parent_area',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='worldbuilder.Area'),
        ),
    ]