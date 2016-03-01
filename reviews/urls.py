from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),

    # ex: /hiring_detail/5/
    url(r'^hiring_detail/(?P<hire_id>[0-9]+)/$',views.hiring_detail, name='hiring_detail')


]
