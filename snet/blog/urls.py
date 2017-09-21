from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.post_view, name='post_view'),
    url(r'^(?P<post_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^(?P<post_id>[0-9]+)/edit/$', views.update, name='update'),
    url(r'^(?P<post_id>[0-9]+)/delete/$', views.delete, name='delete'),
]