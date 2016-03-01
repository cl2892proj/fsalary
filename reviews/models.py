from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hire(models.Model):
    employer_name = models.CharField(max_length=128)
    wage_rate = models.FloatField() 
    wage_unit_of_pay = models.CharField(max_length=64,null=True)
    job_title = models.CharField(max_length=128,null=True)
    start_date = models.DateField()

    def __unicode__(self):
        return str(self.id)


class Review(models.Model):
    hire = models.ForeignKey(Hire)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=400)


