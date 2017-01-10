from django.contrib import admin

from . import models



class LanguageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(models.Language, LanguageAdmin)