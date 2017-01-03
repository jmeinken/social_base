

from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^ajax/posts/edit/(?P<post_id>[0-9]+)', views.ajax_edit_post, name='ajax_edit_post'),
   url(r'^ajax/posts/delete/(?P<post_id>[0-9]+)', views.ajax_delete_post, name='ajax_delete_post'),
   url(r'^ajax/posts/(?P<post_id>[0-9]+)/comments/new', views.ajax_new_comment, name='ajax_new_comment'),
   url(r'^ajax/posts', views.ajax_posts, name='ajax_posts'),
   url(r'^ajax/comments/edit/(?P<comment_id>[0-9]+)', views.ajax_edit_comment, name='ajax_edit_comment'),
   url(r'^ajax/comments/delete/(?P<comment_id>[0-9]+)', views.ajax_delete_comment, name='ajax_delete_comment'),
   
   # new methods
   url(r'^home2', views.home2, name='home2'),
   url(r'^posts/(?P<post_id>[0-9]+)', views.view_post, name='view_post'),
   url(r'^posts/new', views.new_post, name='new_post'),
   url(r'^posts/edit/(?P<post_id>[0-9]+)', views.edit_post, name='edit_post'),
   url(r'^posts/delete/(?P<post_id>[0-9]+)', views.delete_post, name='delete_post'),
   
   #url(r'^comments/new', views.new_comment, name='new_comment'),
   #url(r'^comments/edit', views.edit_comment, name='edit_comment'),
   #url(r'^comments/delete', views.delete_comment, name='delete_comment'),
   
   
]