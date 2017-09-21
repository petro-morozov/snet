from django.conf.urls import url
from . import views

app_name = 'user_page'
urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)$',  views.user_page, name='user_page'),
    url(r'^show_all_users/$', views.show_all_users, name='show_all_users'),
    url(r'^show_fellows_list/$', views.show_fellows_list, name='show_fellows_list'),
    url(r'^fellows_list/(?P<user_id>[0-9]+)/$', views.fellows_list, name='fellows_list'),
]
