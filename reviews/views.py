from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import OflcPerm, OflcPerm_Review
from .forms import ReviewForm
import datetime
import pdb

#haystack begin

from haystack.generic_views import FacetedSearchView
#haystack end

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

def index(request):
    pass
    #context = {'form':}
    #return render(request, 'reviews/index.html', context)

def wage_unit_std(unit):
    """used to standardize unit text for wage"""
    try:
        return WAGE_UNIT_MAP[unit.lower()]
    except:
        return unit
    
def min_date(date_list):
    try:
        return min(filter(lambda x: x is not None, date_list))
    except:
        return None

def hiring_detail(request, year, case_number):
    perm = get_object_or_404(OflcPerm, year=year, case_number=case_number)

    hire = {
                'year':perm.year,
                'case_number':perm.case_number,
                'job_title':perm.job_info_job_title,
                'start_date':min_date([perm.decision_date, perm.case_received_date]) or '',
                'wage': perm.pw_amount_9089 or perm.wage_offer_from_9089,
                'wage_unit': wage_unit_std(perm.pw_unit_of_pay_9089 or perm.wage_offer_unit_of_pay_9089), 
                'employer_name':perm.employer_name or '',
                'employer_address1':perm.employer_address_1 or '',
                'employer_address2':perm.employer_address_2 or '',
                'employer_city':perm.employer_city or '',
                'employer_state':perm.employer_state or '',
                'employer_zipcode':perm.employer_postal_code or '',
                'employer_num_employees':perm.employer_num_employees or '',
                'employer_yr_estab':perm.employer_yr_estab or '',
                'education': perm.job_info_education or '',
                'major': perm.job_info_major or '',
                'class_of_admission': perm.class_of_admission,
            }
    review_list = OflcPerm_Review.objects.filter(perm = perm)
    context = {'source':'perm', 'hire':hire, 'review_list':review_list, 'form':ReviewForm()}
    return render(request, 'reviews/hiring_detail.html', context)
    
def add_review(request, year, case_number):
    perm = get_object_or_404(OflcPerm, year=year, case_number=case_number)
    form = ReviewForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        review = OflcPerm_Review()
        review.perm = perm
        review.pub_date = datetime.datetime.now()
        review.user_name = 'user1'
        review.comment = comment
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:hiring_detail', args=(year, case_number)))
    review_list = Review.objects.filter(hire_id=hire_id)
    context = {'hire':hire, 'review_list':review_list, 'form':form}
    return render(request, 'reviews/hiring_detail.html',context)
        

class MyFacetedSearchView(FacetedSearchView):
    #pdb.set_trace()
    facet_fields = ['employer_name','employer_address1']

