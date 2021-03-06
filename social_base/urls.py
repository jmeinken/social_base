"""social_base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^account/', include('allauth.urls')),
    
    url(r'^images/', include('images.urls', namespace="images")),
    url(r'^email_handler/', include('email_handler.urls', namespace="email_handler")),
    url(r'^microfeed2/', include('microfeed2.urls', namespace="microfeed2")),
    url(r'^pages/', include('pages.urls', namespace="pages")),
    url(r'^field_trans/', include('field_trans.urls', namespace="field_trans")),
    url(r'^', include('main.urls')),
    
]


