import datetime
from haystack import indexes
from .models import *

class Hires_Index(indexes.SearchIndex):
    employment_confirmed = indexes.BooleanField(model_attr='employment_confirmed',faceted=True) 
    employer_name = indexes.CharField(model_attr='employer_name',faceted=True,null=True)
    work_location = indexes.CharField(model_attr='get_work_location',faceted=True,null=True)
    job_title = indexes.CharField(model_attr='job_title',faceted=True,null=True)
    start_date = indexes.DateField(model_attr='get_start_date',faceted=True,null=True)
    base_salary = indexes.CharField(model_attr='get_base_salary',null=True)
    annual_base_salary = indexes.CharField(model_attr='get_annual_base_salary',null=True)
    unit = indexes.CharField(model_attr='get_unit',faceted=True,null=True)
    url = indexes.CharField(model_attr='get_absolute_url',null=True)

    #auto complete
    #content_auto = indexes.EdgeNgramField(model_attr='employer_address_1')


    class Meta:
        abstract = True

    #per document: if specified, this is used by the reindex command to filter out results from the queryset, enabling you to reindex only recent records. This method should either return None
    def get_updated_field(self):
        return "updated_time"

    def get_model(self):
        raise NotImplementedError('Subclasses should implement this!')

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class Hires_Perm_Index(Hires_Index, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Hires_Perm

class Hires_H1B_Index(Hires_Index, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Hires_H1B

class Hires_H2A_Index(Hires_Index, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Hires_H2A

class Hires_H2B_Index(Hires_Index, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Hires_H2B
