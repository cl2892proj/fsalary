"""fsalary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from reviews.views import MyFacetedSearchView, filter_results


#haystack begin
#from haystack.forms import FacetedSearchForm
#from haystack.views import FacetedSearchView
#haystack end

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^accounts/',include('django.contrib.auth.urls',namespace='auth')),

    #haystack search
    url(r'^$', MyFacetedSearchView.as_view(), name="haystack_search"),
    url(r'^filter/', filter_results, name='filter_results'),
]

