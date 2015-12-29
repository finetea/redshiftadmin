from django.contrib import admin
from redshift.models import DBConnection, DBQuery
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.

class AdminDBConnection(admin.ModelAdmin):
    list_display = ("title", )
    search_fields = ("title", )
    
class AdminDBQuery(admin.ModelAdmin):
    list_display = ("title", )
    search_fields = ("title", )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':28, 'cols':200})},
    }
        
admin.site.register(DBConnection, AdminDBConnection, )    
admin.site.register(DBQuery, AdminDBQuery, )
