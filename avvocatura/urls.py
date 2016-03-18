from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hosts/$', views.hosts_index, name='hosts_index'),
    url(r'^servizi/$', views.servizi_index, name='servizi_index'),
    url(r'^hosts/(?P<id>[a-zA-Z0-9_]+)/$', views.detail, name='detail'),
    url(r'^servizi/(?P<id>[a-zA-Z0-9_]+)/$', views.service_detail, name='service_detail'),
    #url(r'^hosts/$', views.service_detail, name='service_detail'),

]