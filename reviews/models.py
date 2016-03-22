from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Hire(models.Model):
    year = models.IntegerField()
    employer_name = models.TextField()
    employer_address1 = models.TextField()
    employer_address2 = models.TextField()
    employer_city = models.TextField()
    employer_state = models.TextField()
    employer_postal_code = models.TextField()
    job_title = models.TextField()
    wage = models.FloatField()
    unit_of_pay = models.TextField()
    source = models.TextField()

    class Meta:
        managed = False
        db_table = 'reviews_hire'

class Review(models.Model):
    hire = models.ForeignKey(Hire)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=400)


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

class OflcPerm(models.Model):
    year = models.IntegerField()
    case_number = models.TextField()
    decision_date = models.DateField()
    case_status = models.TextField()
    case_received_date = models.DateField()
    employer_name = models.TextField()
    employer_address_1 = models.TextField()
    employer_address_2 = models.TextField()
    employer_city = models.TextField()
    employer_state = models.TextField()
    employer_country = models.TextField()
    employer_postal_code = models.TextField()
    employer_num_employees = models.FloatField()
    employer_yr_estab = models.FloatField()
    pw_amount_9089 = models.FloatField()
    pw_unit_of_pay_9089 = models.TextField()
    wage_offer_from_9089 = models.FloatField()
    wage_offer_to_9089 = models.FloatField()
    wage_offer_unit_of_pay_9089 = models.TextField()
    job_info_job_title = models.TextField()
    job_info_education = models.TextField()
    job_info_major = models.TextField()
    class_of_admission = models.TextField()
