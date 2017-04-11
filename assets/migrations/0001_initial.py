# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('asset_type', models.CharField(choices=[('S', 'satellite'), ('A', 'antenna')], max_length=1)),
                ('asset_class', models.CharField(choices=[('D', 'dove'), ('R', 'rapideye'), ('I', 'dish'), ('Y', 'yagi')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='AssetDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('val_type', models.CharField(choices=[('F', 'float'), ('B', 'boolean'), ('I', 'integer'), ('S', 'string')], editable=False, max_length=1)),
                ('val', models.TextField(blank=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
        ),
    ]