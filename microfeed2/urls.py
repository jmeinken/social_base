

from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^ajax/posts/edit/(?P<post_id>[0-9]+)', views.ajax_edit_post, name='ajax_edit_post'),
   url(r'^ajax/posts', views.ajax_posts, name='ajax_posts'),
   
]