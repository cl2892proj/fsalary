from django.contrib import admin

# Register your models here.
from .models import Hires_Perm, Hires_H1B, Hires_H1B_Review, Hires_Perm_Review



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name','comment','pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']

class ReviewH1BAdmin(ReviewAdmin):
    model = Hires_H1B_Review 

class ReviewPermAdmin(ReviewAdmin):
    model = Hires_Perm_Review 

admin.site.register(Hires_Perm)
admin.site.register(Hires_H1B)
admin.site.register(Hires_Perm_Review, ReviewPermAdmin)
admin.site.register(Hires_H1B_Review, ReviewH1BAdmin)
