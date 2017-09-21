from django.contrib import admin
from .models import Room, Message


admin.site.register(
    Room,
    list_display=["id"],
    list_display_links=["id"],
)
admin.site.register(Message)