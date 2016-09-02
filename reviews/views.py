from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Hires_Perm, Hires_H1B, Hire_Review
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

    
def min_date(date_list):
    try:
        return min(filter(lambda x: x is not None, date_list))
    except:
        return None

def hire_detail(request, pid, source):
    if source == 'H1B':
        job = get_object_or_404(Hires_H1B, pid = pid )
        data_source = 'H1B Public Disclosure'
    elif source == 'PERM':
        job = get_object_or_404(Hires_Perm, pid = pid )
        data_source = 'PERM Public Disclosure'
    else:
        print source + ' is an unexpected source'


    hire = {
                'source':data_source,
                'job_title':job.job_title,
                'employer':job.employer_name, 
                'employer_address1':job.employer_address1, 
                'employer_address2':job.employer_address2, 
                'employer_city':job.employer_city,
                'employer_state':job.employer_state,
                'employer_postal_code':job.employer_postal_code,
                'wage_from_1':job.wage_from_1 ,
                'wage_to_1':job.wage_to_1 ,
                'rate_unit_1':job.get_unit() ,
                'annualized_rate': job.get_annual_base_salary(),

                'employment_start_date':job.get_start_date(),
                'work_location_city1':job.work_location_city1,
                'work_location_state1':job.work_location_state1, 

            }
    review_list = Hire_Review.objects.filter(
                employer_name = job.employer_name,
                job_title = job.job_title,
                year = job.get_start_date().year,
                salary = job.get_base_salary(),
                job_date = job.get_start_date(),
            )
    context = {'hire':hire, 'review_list':review_list, 'form':ReviewForm()}
    return render(request, 'reviews/h1b_detail.html', context)

@login_required
def add_review(request, employer_name, job_title, job_date, salary):
    #job_date is in the form yyyymmdd
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = Hire_Review()
        review.employer_name = employer_name
        review.job_title = job_title
        review.salary = salary
        review.job_date = datetime.datetime.strptime(job_date, '%Y%m%d').date()
        review.pub_date = datetime.datetime.now()
        review.user_name = request.user.username 
        review.comment = form.cleaned_data['comment'] 
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:hiring_detail', args=(source, pid)))
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
            'work_location',
            'job_title',
            'start_date',
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
