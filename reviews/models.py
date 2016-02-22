from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hire(models.Model):
    employer_name = models.CharField(max_length=128)
    employer_addr = models.CharField(max_length=128)
    employer_city = models.CharField(max_length=64)
    employer_state = models.CharField(max_length=64)
    wage_rate = models.FloatField() 
    wage_unit_of_pay = models.CharField(max_length=64)
    work_city = models.CharField(max_length=64)
    work_state = models.CharField(max_length=64)
    job_title = models.CharField(max_length=128)
    start_date = models.DateField()
    disclosure_file = models.CharField(max_length=128)
    oflc_program_name = models.CharField(max_length=64)
    fiscal_year = models.IntegerField()

