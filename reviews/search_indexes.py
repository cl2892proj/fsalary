import datetime
from haystack import indexes
from .models import OflcPerm, OflcH1B

class OflcPermIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    year = indexes.IntegerField(model_attr='year',faceted=True,)
    case_status = indexes.CharField(model_attr='case_status',faceted=True,null=True)
    employer_name = indexes.CharField(model_attr='employer_name',faceted=True,null=True)
    employer_address1 = indexes.CharField(model_attr='employer_address1',faceted=True,null=True)
    employer_city = indexes.CharField(model_attr='employer_city',faceted=True,null=True)
    employer_state = indexes.CharField(model_attr='employer_state',faceted=True,null=True)
    employer_postal_code = indexes.CharField(model_attr='employer_postal_code',faceted=True,null=True)
    job_title = indexes.CharField(model_attr='job_title',faceted=True,null=True)
    job_info_education = indexes.CharField(model_attr='job_info_education',null=True)
    job_info_major = indexes.CharField(model_attr='job_info_major',null=True)
    class_of_admission = indexes.CharField(model_attr='class_of_admission',null=True)
    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')

    def get_model(self):
        return OflcPerm

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class OflcH1BIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    year = indexes.IntegerField(model_attr='year',faceted=True,)
    case_status = indexes.CharField(model_attr='case_status',faceted=True,)
    employer_name = indexes.CharField(model_attr='employer_name',faceted=True,null=True)
    employer_address1 = indexes.CharField(model_attr='employer_address1',faceted=True,null=True)
    employer_city = indexes.CharField(model_attr='employer_city',faceted=True,null=True)
    employer_state = indexes.CharField(model_attr='employer_state',faceted=True,null=True)
    employer_postal_code = indexes.CharField(model_attr='employer_postal_code',faceted=True,null=True)
    job_title = indexes.CharField(model_attr='job_title',faceted=True,null=True)
    worksite_city = indexes.CharField(model_attr='worksite_city',null=True)
    worksite_state = indexes.CharField(model_attr='worksite_state',null=True)
    worksite_postal_code = indexes.CharField(model_attr='worksite_postal_code',null=True)

    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')

    def get_model(self):
        return OflcH1B

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
