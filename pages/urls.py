from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [

    
    url(r'^new', views.new_page, name='new_page'),
    url(r'^delete', views.delete_page, name='delete_page'),
    url(r'^edit/(?P<page_id>[0-9]+)', views.edit_page, name='edit_page'),
    url(r'^translate/(?P<page_id>[0-9]+)', views.translate_page, name='translate_page'),
    url(r'^view/(?P<page_id>[0-9]+)', views.view_page, name='view_page'),
    url(r'^list/(?P<page_category_id>[0-9]+)', views.list, name='list'),
    
    url(r'^categories/new', views.new_category, name='new_category'),
    url(r'^categories/edit/(?P<category_id>[0-9]+)', views.edit_category, name='edit_category'),
    url(r'^categories/translate/(?P<category_id>[0-9]+)', views.translate_category, name='translate_category'),
]