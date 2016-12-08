from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url(r'^posts/view/(?P<post_id>[0-9]+)', views.view_post, name='view_post'),
    
    url(r'^posts/new', views.new_post, name='new_post'),
    url(r'^posts/edit', views.edit_post, name='edit_post'),
    url(r'^posts/delete', views.delete_post, name='delete_post'),
    
    url(r'^posts/comments/new', views.new_comment, name='new_comment'),
    url(r'^posts/comments/edit', views.edit_comment, name='edit_comment'),
    url(r'^posts/comments/delete', views.delete_comment, name='delete_comment'),
    
    url(r'^posts/(?P<post_id>[0-9]+)', views.get_post, name='get_post'),
    url(r'^ajax/posts', views.ajax_posts, name='ajax_posts'),
    
    url(r'^events/new', views.new_event, name='new_event'),
    url(r'^events/edit/(?P<post_id>[0-9]+)', views.edit_event, name='edit_event'),
    
    # url(r'^javascript_templates', views.javascript_templates, name='javascript_templates'),
]