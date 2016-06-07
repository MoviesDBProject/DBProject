from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^not_found/', views.page_not_found, name='page_not_found'),
    url(r'^$', views.index, name='index'),

]