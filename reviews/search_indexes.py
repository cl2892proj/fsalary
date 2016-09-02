import datetime
from haystack import indexes
from .models import Hires_Perm, Hires_H1B

class Hires_Perm_Index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    employer_name = indexes.CharField(model_attr='employer_name',faceted=True,null=True)
    work_location = indexes.CharField(model_attr='get_work_location',faceted=True,null=True)
    job_title = indexes.CharField(model_attr='job_title',faceted=True,null=True)
    start_date = indexes.DateField(model_attr='get_start_date',faceted=True,null=True)

    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')

    def get_model(self):
        return Hires_Perm

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class Hires_H1B_Index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    employer_name = indexes.CharField(model_attr='employer_name',faceted=True,null=True)
    work_location = indexes.CharField(model_attr='get_work_location',faceted=True,null=True)
    job_title = indexes.CharField(model_attr='job_title',faceted=True,null=True)
    start_date = indexes.DateField(model_attr='get_start_date',faceted=True,null=True)

    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')

    def get_model(self):
        return Hires_H1B

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
