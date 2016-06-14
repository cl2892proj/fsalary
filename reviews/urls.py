from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /hiring_detail/5/
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/$',views.hiring_detail, name='hiring_detail'),

    # ex: /hiring_detail/data_perm/year/case_number/
    url(r'^hiring_detail/data_perm/(?P<year>[0-9]{4})/(?P<case_number>[a-zA-Z0-9-]+)/(?P<case_status>[a-zA-Z-]+)/$',views.perm_detail, name='perm_detail'),

    
    url(r'^hiring_detail/data_h1b/(?P<year>[0-9]{4})/(?P<case_no>[a-zA-Z0-9-]+)/(?P<case_status>[a-zA-Z-]+)/(?:wage-(?P<prevailing_wage>\d*\.?\d*)/)(?:payfrom-(?P<wage_rate_of_pay_from>\d*\.?\d*)/)$',views.h1b_detail, name='h1b_detail'),
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),

    url(r'^hiring_detail/data_perm/(?P<year>[0-9]{4})/(?P<case_number>[a-zA-Z0-9-]+)/add_review/$', views.add_review, name='add_review'),

]
