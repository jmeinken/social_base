from __future__ import unicode_literals

from django.db import models
from django.conf.settings import AUTH_USER_MODEL


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class Category(TimeStampedModel):
    id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=60, blank=True, null=True)
    
class EmailSettings(TimeStampedModel):
    IMMEDIATE = 'immediate'
    DAILY_DIGEST = 'daily digest'
    NEVER = 'never'
    EMAIL_OPTIONS = (
        (IMMEDIATE, 'immediate'),
        (DAILY_DIGEST, 'daily digest'),
        (NEVER, 'never'),
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    selection = models.CharField(max_length=20, choices=EMAIL_OPTIONS, default=IMMEDIATE)


class Notification(TimeStampedModel):
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    html_short = models.TextField()
    html_long = models.TextField()
    plain_text_short = models.TextField()
    plain_text_long = models.TextField()
    image = models.CharField(max_length=500, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    
class NotificationRecipient(TimeStampedModel):
    notification = models.ForeignKey('Notification', on_delete=models.CASCADE)
    recipient = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    alert_viewed = models.BooleanField(default=False)
    alert_queue = models.BooleanField(default=True)
    email_queue = models.BooleanField(default=True)
    alert_action = models.TextField(blank=True, null=True)
    email_action = models.TextField(blank=True, null=True)
    
    
    
    
    
    
    
    
    