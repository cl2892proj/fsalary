from django.forms import ModelForm, Textarea
from haystack.forms import SearchForm
from collections import defaultdict
import pdb

# The key here is to use the ModelForm factory function
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
