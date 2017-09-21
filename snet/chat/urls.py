from django.conf.urls import include, url
from . import views

app_name = 'chat'
urlpatterns = [
    url(r'^room/(?P<room_id>[0-9]+)/$', views.chat_room, name='chat_room'),
    url(r'^messages_list/(?P<room_id>[0-9]+)/(?P<plscount>[0-9]+)/$', views.messages_list, name='messages_list'),
    url(r'^cr/(?P<user_id>[0-9]+)/$', views.create_room, name='create_room'),
    url(r'^user_rooms/$', views.user_rooms, name='user_rooms'),
]
