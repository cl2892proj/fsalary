from django.forms import ModelForm, Textarea
from reviews.models import OflcPerm_Review 
from haystack.forms import SearchForm
from collections import defaultdict
import pdb

class ReviewForm(ModelForm):
    class Meta:
        model = OflcPerm_Review 
        fields = ['comment',]
        widgets = {
            'comment': Textarea(attrs={ 'cols':40, 
                                        'rows':5,
                                        'maxlength':400, 
                                        'class':"form-control",
                                        'placeholder':'comment',
                                        
                                        }) 
        }


class MultiFacetedSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(MultiFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(MultiFacetedSearchForm, self).search()

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
