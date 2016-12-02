from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
   url(r'^private', views.home_private, name='home_private'),
   url(r'^login', views.login_view, name='login'),
   url(r'^logout', views.logout_view, name='logout'),
   url(r'^create_account', views.create_account, name='create_account'),
   url(r'^account_settings', views.account_settings, name='account_settings'),
   url(r'^forgot_password', views.forgot_password, name='forgot_password'),
   url(r'^$', views.home, name='home')
]