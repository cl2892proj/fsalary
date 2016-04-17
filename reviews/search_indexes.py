import datetime
from haystack import indexes
from .models import OflcPerm

class OflcPermIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    employer_name = indexes.CharField(model_attr='employer_name', null=True, faceted=True) 
    employer_address_1 = indexes.CharField(model_attr='employer_address_1', null=True, faceted=True ) 
    #pub_date = indexes.DateTimeField(model_attr='pub_date')

    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')

    def get_model(self):
        return OflcPerm

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
