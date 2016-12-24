from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import MultiFacetedSearchForm
import datetime
import time
import pdb
from django.utils import timezone
from .models import * 
from django.forms import Textarea


#ModelForm Factory Function
from django.forms import modelform_factory

#charting
import random
from django.shortcuts import render_to_response

#haystack begin

from haystack.generic_views import FacetedSearchView
#haystack end

def modelBySource(source, group):
    #both inputs are strings
    if group == 'REVIEW':
        if source == 'H1B':
            model = Hires_H1B_Review
        elif source == 'PERM':
            model = Hires_Perm_Review
        elif source == 'H2A':
            model = Hires_H2A_Review
        elif source == 'H2B':
            model = Hires_H2B_Review
        else:
            print '##### ERROR #####'
            print source + ' is an unexpected source'
            print '##### ERROR #####'
    elif group == 'HIRE':
        if source == 'H1B':
            model = Hires_H1B
        elif source == 'PERM':
            model = Hires_Perm
        elif source == 'H2A':
            model = Hires_H2A
        elif source == 'H2B':
            model = Hires_H2B
        else:
            print '##### ERROR #####'
            print source + ' is an unexpected source'
            print '##### ERROR #####'
    else:
        print "incorrect group"
    return model

def reviewFormFactory(source):
    model = modelBySource(source,'REVIEW')

    # The key here is to use the ModelForm factory function
    ReviewForm = modelform_factory( 
            model,
            fields = ['comment',], 
            widgets = {
                'comment': Textarea(attrs={ 'cols':40, 
                                            'rows':5,
                                            'maxlength':400, 
                                            'class':"form-control",
                                            'placeholder':'comment',
                                            
                                            })} 
            )
    return ReviewForm


def min_date(date_list):
    try:
        return min(filter(lambda x: x is not None, date_list))
    except:
        return None

def hire_detail(request, pid, source):
    data_source = source
    hire = get_object_or_404(modelBySource(source,'HIRE'), pid = pid )

    context = {'source':data_source, 'pid':pid, 'hire':hire} 
    return render(request, 'reviews/hiring_detail.html', context)

#@login_required
def add_review(request, source, pid):
    #job_date is in the form yyyymmdd
    print '-----------'
    print source
    
    hire = get_object_or_404(modelBySource(source,'HIRE'), pid = pid )

    ReviewForm = reviewFormFactory(source)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = modelBySource(source,'REVIEW')()
        review.hire = hire
        review.pub_date = timezone.now()
        review.user_name = request.user.username 
        review.comment = form.cleaned_data['comment'] 
        review.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('reviews:hire_detail', args=(source, pid)))

def filter_results(request):
    if request.method == 'GET':
        form = FilterForm(request.GET)
        if form.is_valid():
            print '{0}&selected_facets=employer_name_exact:'.format(request.get_full_path,)
            #return HttpResponseRedirect(reverse('haystack_search'))


class MyFacetedSearchView(FacetedSearchView):
    #### The main search result view ####

    facet_fields = [
            'employer_name',
            'work_location',
            'job_title',
            'start_date',
        ]

    facet_date_fields = [
            'start_date',
            ]

    
    form_class = MultiFacetedSearchForm

    def get_context_data(self, **kwargs):

        context = super(FacetedSearchView, self).get_context_data(**kwargs)

        #### Bring in the results START ####

        result_list = map(lambda x: x.get_additional_fields(), context['object_list'])


        results = map(lambda x:{  
            'employer_name': x.get('employer_name',''),
            'job_title': x.get('job_title',''),
            'base_salary':x.get('base_salary',0),
            'unit':x.get('unit',''),
            'work_location':x.get('work_location',''),
            'start_date':x.get('start_date',''),
            'url':x.get('url',''),
                        }, result_list)

        context['results'] = results

        #### Bring in the results END ####

        #### FACETING START #### 
        context['facet_fields'] = self.facet_fields
        context['facet_date_fields'] = self.facet_date_fields
        #### FACETING END #### 

        #### SCATTER CHART START #### 
        #qs = super(FacetedSearchView, self).get_queryset()
        #all_results = map(lambda x: x.get_additional_fields(), qs)

        #xdata = map(lambda x: x['start_date'], all_results)
        #xdata = map(lambda x: int(time.mktime(x.timetuple()))*1000, xdata)
        #ydata1 = map(lambda x: x['annual_base_salary'], all_results)

        ##pdb.set_trace()

        #kwargs1 = {'shape': 'triangle-up'}

        #extra_serie1 = {"tooltip": {"y_start": "", "y_end": "balls"}}

        #chartdata = {
        #    'x': xdata,

        #    'name1': 'base salary', 
        #    'y1': ydata1, 
        #    'kwargs1': kwargs1, 
        #    'extra1': extra_serie1,
        #}

        ##charttype = "discreteBarChart"
        ##chartcontainer = 'discretebarchart_container'  # container name
        #charttype = "lineChart"
        #chartcontainer = 'linechart_container'  # container name
        ##charttype = "scatterChart"
        ##chartcontainer = 'scatterchart_container'  # container name
        #context['charttype'] = charttype 
        #context['chartdata'] = chartdata 
        #context['chartcontainer'] = chartcontainer
        #context['d3_extra'] =  {
        #        'x_is_date': True,
        #        'x_axis_format': '%d %b %Y',
        #        'tag_script_js': True,
        #        'jquery_on_ready': True,
        #    }

        #### SCATTER CHART END #### 


        #### PAGINATION START #### 
        NUM_VISIBLE = 5

        page_curr = context['page_obj'].number
        page_last = context['page_obj'].paginator.num_pages




        if page_last > NUM_VISIBLE:
            i, j = 0, 0
            while i + j < NUM_VISIBLE:
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
        

        #list of page numbers that should show up between the dot dot dot
        context['pages_visible'] = pages_visible
        #boolean variable on if showing the first set of dot dot dot
        context['first_dotdotdot'] = first_dotdotdot
        #boolean variable on if showing the second set of dot dot dot
        context['last_dotdotdot'] = last_dotdotdot

        #### PAGINATION END #### 
        
        return context
