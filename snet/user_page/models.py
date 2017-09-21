from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class OnlineUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user', primary_key=True,)
    online = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

class UserPic(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_pic', primary_key=True,)
    image = models.ImageField(null=True, blank=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

class UPText(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_page_text', primary_key=True,)
    text = models.TextField(max_length=700, null=True)