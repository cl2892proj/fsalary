from django import forms
from django.forms import ModelForm, Textarea
from haystack.forms import SearchForm
from collections import defaultdict
import pdb


class MultiFacetedSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(MultiFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(MultiFacetedSearchForm, self).search().order_by('-start_date_exact')

        facet_dict = defaultdict(list)

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            facet_dict[field].append(value)

        for field, value_list in facet_dict.iteritems():
            if value_list:
                sqs = sqs.narrow(" OR ".join(map(lambda x:u'%s:"%s"' % (field,sqs.query.clean(x)) ,value_list)))

        return sqs


class UserProfileForm(forms.Form):
    #http://stackoverflow.com/questions/12303478/how-to-customize-user-profile-when-using-django-allauth
    #customized user profile form using allauth

    first_name = forms.CharField(max_length=30, label='Voornaam')
    last_name = forms.CharField(max_length=30, label='Achternaam')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
    

