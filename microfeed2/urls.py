

from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^ajax/posts', views.ajax_posts, name='ajax_posts'),
]