from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OflcH1B(models.Model):
    year = models.IntegerField()
    case_no = models.TextField()
    case_status = models.TextField()
    case_submitted = models.DateField()
    employment_start_date = models.DateField()
    employment_end_date = models.DateField()
    employer_name = models.TextField()
    employer_address1 = models.TextField()
    employer_address2 = models.TextField()
    employer_city = models.TextField()
    employer_state = models.TextField()
    employer_postal_code = models.TextField()
    employer_country = models.TextField()
    employer_province = models.TextField()
    employer_phone = models.TextField()
    employer_phone_ext = models.TextField()
    job_title = models.TextField()
    soc_name = models.TextField()
    full_time_position = models.TextField()
    prevailing_wage = models.FloatField()
    pw_unit_of_pay = models.TextField()
    wage_rate_of_pay_from = models.FloatField()
    wage_rate_of_pay_to = models.FloatField()
    wage_unit_of_pay = models.TextField()
    worksite_city = models.TextField()
    worksite_county = models.TextField()
    worksite_state = models.TextField()
    worksite_postal_code = models.TextField()
    lca_case_workloc2_city = models.TextField()
    lca_case_workloc2_state = models.TextField()
    pw_2 = models.FloatField()
    pw_unit_2 = models.TextField()

    class Meta:
        unique_together = ('year', 'case_no')

class OflcH1B_Review(models.Model):
    h1b = models.ForeignKey(OflcH1B)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=30)
    comment = models.CharField(max_length=1000)

class OflcPerm(models.Model):
    year = models.IntegerField()
    case_number = models.TextField()
    decision_date = models.DateField(null=True)
    case_status = models.TextField(null=True)
    case_received_date = models.DateField(null=True)
    employer_name = models.TextField(null=True)
    employer_address_1 = models.TextField(null=True)
    employer_address_2 = models.TextField(null=True)
    employer_city = models.TextField(null=True)
    employer_state = models.TextField(null=True)
    employer_country = models.TextField(null=True)
    employer_postal_code = models.TextField(null=True)
    employer_num_employees = models.FloatField(null=True)
    employer_yr_estab = models.FloatField(null=True)
    pw_amount_9089 = models.FloatField(null=True)
    pw_unit_of_pay_9089 = models.TextField(null=True)
    wage_offer_from_9089 = models.FloatField(null=True)
    wage_offer_to_9089 = models.FloatField(null=True)
    wage_offer_unit_of_pay_9089 = models.TextField(null=True)
    job_info_job_title = models.TextField(null=True)
    job_info_education = models.TextField(null=True)
    job_info_major = models.TextField(null=True)
    class_of_admission = models.TextField(null=True)

    class Meta:
        unique_together = ('year', 'case_number', 'case_status')
    
    
class OflcPerm_Review(models.Model):
    perm = models.ForeignKey(OflcPerm)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=30)
    comment = models.CharField(max_length=1000)

