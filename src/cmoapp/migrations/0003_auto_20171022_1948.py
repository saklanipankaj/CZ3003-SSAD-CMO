# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-22 11:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmoapp', '0002_auto_20171022_0110'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
