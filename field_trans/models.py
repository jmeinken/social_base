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
    language             = models.ForeignKey('Language', on_delete=models.PROTECT)
    text                 = models.TextField()
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        unique_together = (("table_name", "field_name", "field_id", "language"),)
        
class Language(models.Model):
    code            = models.CharField(max_length=6, primary_key=True)
    name            = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
