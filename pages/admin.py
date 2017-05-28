from django.contrib import admin

from . import models




    
class PageLinkAdmin(admin.TabularInline):    # can also use TabularInline
    model = models.PageLink
    extra = 3
    
class PageAdmin(admin.ModelAdmin):
    inlines = [PageLinkAdmin]
    
admin.site.register(models.Page, PageAdmin)

class PageCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.PageCategory, PageCategoryAdmin)
