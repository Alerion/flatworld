from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^world/(?P<world_id>\d+)/$', views.wolrd, name='world'),
]
