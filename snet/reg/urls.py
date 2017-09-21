from django.conf.urls import url

from . import views

app_name = 'reg'
urlpatterns = [
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.login_form, name = 'login'),
    url(r'^logout/$', views.logout_form, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^user_settings/$', views.user_settings, name = 'user_settings'),
]