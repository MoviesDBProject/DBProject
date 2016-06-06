"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from moviestats.queryHandler import *

urlpatterns = [
    url(r'^$', include('moviestats.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^fetch_results/', handle_query),
    url(r'^get_actors_list/', get_actors),
    url(r'^get_directors_list/', get_directors),
    url(r'^get_countries_list/', get_countries),
    url(r'^get_language_list/', get_languages),
    url(r'^404/', include('moviestats.urls')),

]
