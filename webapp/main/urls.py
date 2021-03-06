from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^world/$', views.worlds, name='worlds'),
    url(r'^world/(?P<world_id>\d+)/$', views.world, name='world'),
    url(r'^world/(?P<world_id>\d+)/building/$', views.world, name='building'),
    url(r'^world/(?P<world_id>\d+)/units/$', views.world, name='units'),
    url(r'^world/(?P<world_id>\d+)/quests/$', views.world, name='quests'),
    url(r'^world/(?P<world_id>\d+)/quest-demo/$', views.world, name='quest-demo'),
]
