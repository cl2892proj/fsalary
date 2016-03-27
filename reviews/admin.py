from django.contrib import admin

# Register your models here.
from .models import OflcPerm, OflcPerm_Review

class ReviewAdmin(admin.ModelAdmin):
    model = OflcPerm_Review
    list_display = ('perm','user_name','comment','pub_date')
    list_filter = ['pub_date','user_name']
    search_fields = ['comment']

admin.site.register(OflcPerm)
admin.site.register(OflcPerm_Review, ReviewAdmin)
