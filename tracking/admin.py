from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Visitor

class vistiorAdmin(ModelAdmin):
    list_display = ['ip_address', 'location', 'city', 'country', 'device', 'visit_time']
    
    class Meta:
        model=Visitor
        
admin.site.register(Visitor, vistiorAdmin)