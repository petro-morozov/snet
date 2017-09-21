from django.conf.urls import url
from . import views

app_name = 'fellows'
urlpatterns = [
    url(r'^new_fellow/$', views.add_to_fellows, name='add_to_fellows'),
]
