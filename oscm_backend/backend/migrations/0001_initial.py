# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('version', models.CharField(blank=True, max_length=100, null=True)),
                ('operating_system', models.IntegerField(choices=[(0, 'OS_MAC'), (1, 'OS_LINUX')], default=0)),
                ('architecture', models.IntegerField(choices=[(32, '32-bit'), (32, '64-bit')], default=32)),
                ('value', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
