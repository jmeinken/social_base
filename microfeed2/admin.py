from django.contrib import admin
from . import models


class PostThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(models.PostThread, PostThreadAdmin)

class PostImageAdmin(admin.StackedInline):    # can also use TabularInline
    model = models.PostImage
    extra = 1
    
class PostCommentAdmin(admin.StackedInline):    # can also use TabularInline
    model = models.PostComment
    extra = 1
    
class PostTimeAdmin(admin.StackedInline):
    model = models.PostTime
    extra = 1
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'thread')
    inlines = [PostImageAdmin, PostCommentAdmin, PostTimeAdmin]
    
admin.site.register(models.Post, PostAdmin)


    

    
