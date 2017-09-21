from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Fellows(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_u', null=True)
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_u', null=True)

class ShowFellows(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='show_fellows', primary_key=True,)
    show = models.BooleanField(default=True)