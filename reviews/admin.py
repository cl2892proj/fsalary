from django.contrib import admin

# Register your models here.
from .models import Hires_Perm, Hires_H1B



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name','comment','pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']


admin.site.register(Hires_Perm)
admin.site.register(Hires_H1B)
