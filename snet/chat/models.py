from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()

class Room(models.Model):
    f_usr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='f_u', null=True)
    s_usr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='s_u', null=True)
    f_in_chat = models.BooleanField(default=False)
    s_in_chat = models.BooleanField(default=False)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True, related_name='message')
    text = models.TextField(max_length=1000,null=True)
    image = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    fk = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    saw = models.BooleanField(default=False)

class IsUserInChat(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_in_chat', primary_key=True,)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='user_in_room')
    in_chat = models.BooleanField(default=False)

class IsUserInRoomsPage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_in_rooms_page', primary_key=True,)
    in_rooms_page = models.BooleanField(default=False)

