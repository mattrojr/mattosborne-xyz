# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbilityCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('difficulty', models.FloatField()),
                ('skill', models.CharField(blank=True, max_length=100)),
                ('ability', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AreaConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('area1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start', to='worldbuilder.Area')),
                ('area2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end', to='worldbuilder.Area')),
            ],
        ),
        migrations.CreateModel(
            name='AreaFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldbuilder.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldbuilder.Campaign')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worldbuilder.Region'),
        ),
    ]
