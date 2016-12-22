from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class Image(TimeStampedModel):
    file_base_name = models.CharField(max_length=60, blank=True, null=True)
    app_name = models.CharField(max_length=30, blank=True, null=True)
    model_name = models.CharField(max_length=30, blank=True, null=True)
    uploader = models.CharField(max_length=60, blank=True, null=True)
    
    def get_image_name(self):
        if self.file_base_name:
            base = self.file_base_name
        else:
            base = 'image'
        return base + '_' + str(self.id) + '.png'
    
    def __str__(self):
        return self.get_image_name()

    
class ImageAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Image, ImageAdmin)