from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class OflcH1B(models.Model):
    year = models.IntegerField()
    case_no = models.TextField()
    case_status = models.TextField()
    case_submitted = models.DateField(null=True)
    employment_start_date = models.DateField(null=True)
    employment_end_date = models.DateField(null=True)
    employer_name = models.TextField(null=True)
    employer_address1 = models.TextField(null=True)
    employer_address2 = models.TextField(null=True)
    employer_city = models.TextField(null=True)
    employer_state = models.TextField(null=True)
    employer_postal_code = models.TextField(null=True)
    employer_country = models.TextField(null=True)
    employer_province = models.TextField(null=True)
    employer_phone = models.TextField(null=True)
    employer_phone_ext = models.TextField(null=True)
    job_title = models.TextField(null=True)
    full_time_position = models.TextField(null=True)
    prevailing_wage = models.FloatField(null=True)
    pw_unit_of_pay = models.TextField(null=True)
    wage_rate_of_pay_from = models.FloatField(null=True)
    wage_rate_of_pay_to = models.FloatField(null=True)
    wage_unit_of_pay = models.TextField(null=True)
    worksite_city = models.TextField(null=True)
    worksite_county = models.TextField(null=True)
    worksite_state = models.TextField(null=True)
    worksite_postal_code = models.TextField(null=True)
    lca_case_workloc2_city = models.TextField(null=True)
    lca_case_workloc2_state = models.TextField(null=True)
    pw_2 = models.FloatField(null=True)
    pw_unit_2 = models.TextField(null=True)
    
    def get_absolute_url(self):
        return reverse('reviews:h1b_detail',
                        kwargs={
                            'year':self.year,
                            'case_no':self.case_no,
                            'case_status':self.case_status,
                            'prevailing_wage':self.prevailing_wage or '',
                            'wage_rate_of_pay_from':self.wage_rate_of_pay_from or '',
                                }
                        )

    #def __unicode(self):
    #    return self.job_title


    class Meta:
        unique_together = ('year' 
                            , 'case_no'
                            , 'case_status'
                            , 'prevailing_wage'
                            , 'wage_rate_of_pay_from'
                            )

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
    employer_address1 = models.TextField(null=True)
    employer_address2 = models.TextField(null=True)
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
    job_title = models.TextField(null=True)
    job_info_education = models.TextField(null=True)
    job_info_major = models.TextField(null=True)
    class_of_admission = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('reviews:perm_detail',
                        kwargs={
                            'year':self.year,
                            'case_number':self.case_number,
                            'case_status':self.case_status,
                                }
                        )
    class Meta:
        unique_together = ('year', 'case_number', 'case_status')
    
    
class OflcPerm_Review(models.Model):
    perm = models.ForeignKey(OflcPerm)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=30)
    comment = models.CharField(max_length=1000)

