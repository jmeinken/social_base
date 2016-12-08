from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.utils.timezone import localtime
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _




class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Translation(TimeStampedModel):
    table_name           = models.CharField(max_length=255)
    field_name           = models.CharField(max_length=255)
    field_id             = models.IntegerField()                   
    language             = models.CharField(max_length=32)
    text                 = models.TextField()
    
    def __str__(self):
        return self.text
    
    class Meta:
        unique_together = (("table_name", "field_name", "field_id", "language"),)
