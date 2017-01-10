from django.contrib import admin

from . import models

class UserAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(models.User, UserAdmin)

class LanguageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(models.Language, LanguageAdmin)


