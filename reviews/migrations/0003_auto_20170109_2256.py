# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 03:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_create_unique_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hires_h1b_review',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='hires_h1b_review',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='hires_h2a_review',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='hires_h2a_review',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='hires_h2b_review',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='hires_h2b_review',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='hires_perm_review',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='hires_perm_review',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Hires_H1B_Review',
        ),
        migrations.DeleteModel(
            name='Hires_H2A_Review',
        ),
        migrations.DeleteModel(
            name='Hires_H2B_Review',
        ),
        migrations.DeleteModel(
            name='Hires_Perm_Review',
        ),
    ]
