# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 03:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20160424_2300'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='oflch1b',
            unique_together=set([('year', 'case_no', 'case_status', 'case_submitted', 'employer_name', 'job_title', 'worksite_city', 'employment_start_date', 'employment_end_date')]),
        ),
    ]