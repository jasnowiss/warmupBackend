from django.conf.urls import patterns, url

from loginCounter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^add/$', views.add, name='add'),
)
