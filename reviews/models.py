from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
import datetime, time
import pdb


WAGE_UNIT_MAP = {
                    'hr':'hour',
                    'hour':'hour',

                    'wk':'week',
                    'week':'week',
                    
                    'bi':'bi-week',
                    'bi-weekly':'bi-week',

                    'mth':'month',
                    'month':'month',

                    'yr':'year',
                    'year':'year',
                }

UNIT_MULTIPLIER = {
            'year': 1,
            'month': 12,
            'bi-week': 26,
            'week': 52,
            'hour': 52 * 40,
        }

def wage_unit_std(unit):
    """used to standardize unit text for wage"""
    try:
        return WAGE_UNIT_MAP[unit.lower()]
    except:
        return ''


# The following functions are shared by every table
# so instead of writing a customized codes for every table
# we write the following generic functions
# to use the functions, we simply pass in a list of column headers for each table

def get_start_date(lst):
    for i in lst:
        if i:
            return i

def get_base_salary(lst):
    for i in lst:
        if i:
            return i
    return 0

def get_unit(lst):
    for i in lst:
        if wage_unit_std(i):
            return wage_unit_std(i)
    return ''

def get_work_location(lst):
    #lst is a list of (city, state) tuple
    #the last tuple is always employer city, state
    for i in lst:
        if all(i):
            city = i[0]
            state = i[1]
            return city+', '+state
    employer_city = lst[-1][0] if lst[-1][0] else ''
    employer_state = lst[-1][1] if lst[-1][1] else ''
    return employer_city+', '+employer_state

class Hire_Review(models.Model):
    employer_name = models.TextField(null=True)
    job_title = models.TextField(null=True)
    salary = models.FloatField(null=True)
    job_date = models.DateField(null=True)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=30)
    comment = models.CharField(max_length=1000)
    parent = models.ForeignKey('self',null=True)

class Hires(models.Model):
    source = models.TextField(null=True) #eg. H1B, H2B, Proxy etc
    pid = models.IntegerField(primary_key=True)
    employer_name = models.TextField(null=True)
    employer_address1 = models.TextField(null=True)
    employer_address2 = models.TextField(null=True)
    employer_city = models.TextField(null=True)
    employer_state = models.TextField(null=True)
    employer_postal_code = models.TextField(null=True)
    job_title = models.TextField(null=True)
    wage_from_1 = models.FloatField(null=True)
    wage_to_1 = models.FloatField(null=True)
    rate_unit_1 = models.TextField(null=True)
    std_title = models.TextField(null=True)

    class Meta:
        abstract = True

# Create your models here.
class Hires_H1B(Hires):
    submitted_date = models.DateField(null=True)
    case_number = models.TextField(null=True)
    employment_start_date = models.DateField(null=True)
    pw_1 = models.FloatField(null=True)
    pw_unit_1 = models.TextField(null=True)
    work_location_city1 = models.TextField(null=True)
    work_location_state1 = models.TextField(null=True)
    wage_from_2 = models.FloatField(null=True)
    wage_to_2 = models.FloatField(null=True)
    rate_unit_2 = models.TextField(null=True)
    pw_2 = models.FloatField(null=True)
    pw_unit_2 = models.TextField(null=True)
    work_location_city2 = models.TextField(null=True)
    work_location_state2 = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('reviews:hire_detail',
                        kwargs={
                                    'pid':self.pid,
                                    'source':'H1B',
                                }
                        )
    
    def get_start_date(self):
        return get_start_date(
                    [
                        self.employment_start_date,
                        self.submitted_date,
                    ]
                )

    def get_base_salary(self):
        return get_base_salary(
                    [
                        self.wage_to_1,
                        self.wage_from_1,
                        self.wage_to_2,
                        self.wage_from_2,
                        self.pw_1,
                        self.pw_2,
                    ]
                )

    def get_work_location(self):
        return get_work_location(
                    [
                        (self.work_location_city1, self.work_location_state1),
                        (self.work_location_city2, self.work_location_state2),
                        (self.employer_city, self.employer_state)
                    ] 
                )
    

    def get_unit(self):
        return get_unit(
                    [
                        self.rate_unit_1,
                        self.rate_unit_2,
                        self.pw_unit_1,
                        self.pw_unit_2,
                    ] 
                )

    def get_annual_base_salary(self):
        # return annualized salary for apple to apple comparison
        unit = self.get_unit()
        base = self.get_base_salary()
        return base * UNIT_MULTIPLIER[unit] 

class Hires_Perm(Hires):
    decision_date = models.DateField(null=True) 
    case_number = models.TextField(null=True)
    pw_1 = models.FloatField(null=True)
    pw_unit_1 = models.TextField(null=True)
    work_location_city1 = models.TextField(null=True)
    work_location_state1 = models.TextField(null=True)
    job_info_education  = models.TextField(null=True)
    job_info_major  = models.TextField(null=True)
    country_of_citizenship  = models.TextField(null=True)
    class_of_admission = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('reviews:hire_detail',
                        kwargs={
                                    'pid':self.pid,
                                    'source':'PERM',
                                }
                        )

    def get_start_date(self):
        return get_start_date(
                    [
                        self.decision_date,
                    ]
                )

    def get_base_salary(self):
        return get_base_salary(
                    [
                        self.wage_to_1,
                        self.wage_from_1,
                        self.pw_1,
                    ]
                )

    def get_unit(self):
        return get_unit(
                    [
                        self.rate_unit_1,
                        self.pw_unit_1,
                    ] 
                )

    def get_work_location(self):
        return get_work_location(
                    [
                        (self.work_location_city1, self.work_location_state1),
                        (self.employer_city, self.employer_state)
                    ] 
                )
    def get_annual_base_salary(self):
        # return annualized salary for apple to apple comparison
        unit = self.get_unit()
        base = self.get_base_salary()
        return base * UNIT_MULTIPLIER[unit] 
    
