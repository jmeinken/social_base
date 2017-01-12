from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
   url(r'^composer', views.composer, name='composer'),
   url(r'^unsubscribe/(?P<code>[a-zA-Z0-9]+)', views.unsubscribe, name='unsubscribe'),
]