from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[a-zA-Z0-9_]+)/$', views.detail, name='detail'),
]