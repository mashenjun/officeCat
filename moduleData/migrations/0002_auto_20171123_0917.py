# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-23 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moduleData', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Candidate',
            new_name='User',
        ),
    ]