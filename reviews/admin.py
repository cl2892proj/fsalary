from django.contrib import admin

# Register your models here.
from .models import Hire, Review

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('hire','user_name','comment','pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']

admin.site.register(Hire)
admin.site.register(Review, ReviewAdmin)
