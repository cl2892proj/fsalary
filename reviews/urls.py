from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),

    # ex: /hiring_detail/5/
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/$',views.hiring_detail, name='hiring_detail'),

    # ex: /hiring_detail/data_perm/year/case_number/
    url(r'^hiring_detail/data_perm/(?P<year>[0-9]{4})/(?P<case_number>[a-zA-Z0-9-]+)/$',views.hiring_detail, name='hiring_detail'),
    
    #url(r'^hiring_detail/(?P<hire_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),

    url(r'^hiring_detail/data_perm/(?P<year>[0-9]{4})/(?P<case_number>[a-zA-Z0-9-]+)/add_review/$', views.add_review, name='add_review'),
]
