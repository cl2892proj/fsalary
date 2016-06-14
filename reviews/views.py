from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import OflcPerm, OflcPerm_Review, OflcH1B, OflcH1B_Review
from .forms import ReviewForm, MultiFacetedSearchForm
import datetime
import time
import pdb


#charting
import random
from django.shortcuts import render_to_response

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

def h1b_detail(request, year, case_no,case_status,prevailing_wage,wage_rate_of_pay_from):
    h1b = get_object_or_404(OflcH1B, 
                            year=year, 
                            case_no=case_no,
                            case_status=case_status,
                            prevailing_wage= (None if prevailing_wage =='' else prevailing_wage),
                            wage_rate_of_pay_from=(None if wage_rate_of_pay_from =='' else wage_rate_of_pay_from)
                            )

    hire = {
                'year':h1b.year,
                'case_number':h1b.case_no,
                'job_title':h1b.job_title,
                'start_date':h1b.employment_start_date or '',
                'wage': h1b.wage_rate_of_pay_from or h1b.prevailing_wage,
                'wage_unit': wage_unit_std(h1b.wage_unit_of_pay or h1b.pw_unit_of_pay), 
                'employer_name':h1b.employer_name or '',
                'employer_address1':h1b.employer_address1 or '',
                'employer_address2':h1b.employer_address2 or '',
                'employer_city':h1b.employer_city or '',
                'employer_state':h1b.employer_state or '',
                'employer_zipcode':str(h1b.employer_postal_code).zfill(5),
            }
    review_list = OflcH1B_Review.objects.filter(h1b = h1b)
    context = {'source':'h1b', 'hire':hire, 'review_list':review_list, 'form':ReviewForm()}
    return render(request, 'reviews/hiring_detail.html', context)

def perm_detail(request, year, case_number, case_status):
    perm = get_object_or_404(OflcPerm, year=year, case_number=case_number, case_status=case_status)

    hire = {
                'year':perm.year,
                'case_number':perm.case_number,
                'job_title':perm.job_title,
                'start_date':min_date([perm.decision_date, perm.case_received_date]) or '',
                'wage': perm.pw_amount_9089 or perm.wage_offer_from_9089,
                'wage_unit': wage_unit_std(perm.pw_unit_of_pay_9089 or perm.wage_offer_unit_of_pay_9089), 
                'employer_name':perm.employer_name or '',
                'employer_address1':perm.employer_address1 or '',
                'employer_address2':perm.employer_address2 or '',
                'employer_city':perm.employer_city or '',
                'employer_state':perm.employer_state or '',
                'employer_zipcode':str(perm.employer_postal_code).zfill(5),
                'employer_num_employees':perm.employer_num_employees or '',
                'employer_yr_estab':perm.employer_yr_estab or '',
                'education': perm.job_info_education or '',
                'major': perm.job_info_major or '',
                'class_of_admission': perm.class_of_admission,
            }
    review_list = OflcPerm_Review.objects.filter(perm = perm)
    context = {'source':'perm', 'hire':hire, 'review_list':review_list, 'form':ReviewForm()}
    return render(request, 'reviews/hiring_detail.html', context)

@login_required
def add_review(request, year, case_number):
    perm = get_object_or_404(OflcPerm, year=year, case_number=case_number)
    form = ReviewForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        review = OflcPerm_Review()
        review.perm = perm
        review.pub_date = datetime.datetime.now()
        review.user_name = request.user.username 
        review.comment = comment
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:hiring_detail', args=(year, case_number)))
    review_list = Review.objects.filter(hire_id=hire_id)
    context = {'hire':hire, 'review_list':review_list, 'form':form}
    return render(request, 'reviews/hiring_detail.html',context)
        

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub-date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'review/user_review_list.html', context)

def filter_results(request):
    if request.method == 'GET':
        form = FilterForm(request.GET)
        if form.is_valid():
            print '{0}&selected_facets=employer_name_exact:'.format(request.get_full_path,)
            #return HttpResponseRedirect(reverse('haystack_search'))


class MyFacetedSearchView(FacetedSearchView):
    """
    The main search result view
    """

    facet_fields = [
            'employer_name',
            'employer_address1',
            'employer_city',
            'employer_state',
            'employer_postal_code',
            'job_title',
            'case_status',
            'year',
        ]

    
    form_class = MultiFacetedSearchForm


    
    def get_context_data(self, **kwargs):
        context = super(FacetedSearchView, self).get_context_data(**kwargs)

        """
        facet strings
        """
        context['facet_fields'] = self.facet_fields

        """
        scatterchart page
        """
        start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)

        nb_element = 2 
        xdata = range(nb_element)
        xdata = map(lambda x: start_time + x * 1000000000, xdata)
        #pdb.set_trace()
        ydata = [1,2]
        ydata1 = map(lambda x: x * 2, ydata)
        
        #if not context['object_list']:
        #    pdb.set_trace()
        #    xdata = [result.object.get_start_date() for result in context['object_list']]
        #    ydata1 = [result.object.get_base_salary() for result in context['object_list']]


        kwargs1 = {'shape': 'circle'}

        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}

        chartdata = {
            'x': xdata,
            'name1': 'series 1', 'y1': ydata1, 'kwargs1': kwargs1, 'extra1': extra_serie1,
        }

        #charttype = "discreteBarChart"
        #chartcontainer = 'discretebarchart_container'  # container name
        charttype = "scatterChart"
        chartcontainer = 'scatterchart_container'  # container name
        context['charttype'] = charttype 
        context['chartdata'] = chartdata 
        context['chartcontainer'] = chartcontainer
        context['d3_extra'] =  {
                'x_is_date': True,
                'x_axis_format': '%d %b %Y',
                'tag_script_js': True,
                'jquery_on_ready': True,
            }


        #pagination
        NUM_VISIBLE = 5

        page_curr = context['page_obj'].number
        page_last = context['page_obj'].paginator.num_pages

        if page_last > NUM_VISIBLE:
            i, j = 0, 0
            while i + j <= NUM_VISIBLE:
                if page_curr - i > 1:
                    i += 1
                if page_curr + j < page_last:
                    j += 1
            pages_visible = range(page_curr - i + 1, page_curr + j) 
            first_dotdotdot = (min(pages_visible) > 2)
            last_dotdotdot = (max(pages_visible) < page_last-1)
        else:
            pages_visible = [x+1 for x in range(1, page_last-1)]
            first_dotdotdot = False
            last_dotdotdot = False

        

        context['pages_visible'] = pages_visible
        context['first_dotdotdot'] = first_dotdotdot
        context['last_dotdotdot'] = last_dotdotdot

        
        return context
