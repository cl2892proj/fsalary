# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 02:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='oflch1b',
            unique_together=set([('year', 'case_no', 'case_status', 'case_submitted', 'employer_name')]),
        ),
    ]