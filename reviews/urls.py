from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /hiring_detail/5/
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/$',views.hiring_detail, name='hiring_detail'),

    # ex: /hiring_detail/data_perm/year/case_number/
    url(r'^hiring_detail/(?P<source>\w+)/(?P<pid>\d*)/$',views.hire_detail, name='hire_detail'),

    
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),

    url(r'^hiring_detail/(?P<employer_name>\w+)/(?P<job_title>\w+)/(?P<job_date>\d{4}-\d{2}-\d{2})/(?P<salary>\d*.?\d*)/add_review/$', views.add_review, name='add_review'),

]
