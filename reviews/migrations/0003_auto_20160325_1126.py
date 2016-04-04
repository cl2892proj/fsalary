# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20160325_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oflcperm',
            name='case_number',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='oflcperm',
            name='case_received_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='oflcperm',
            name='case_status',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='oflcperm',
            name='decision_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='oflcperm',
            name='year',
            field=models.IntegerField(),
        ),
    ]