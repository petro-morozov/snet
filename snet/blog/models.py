from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(max_length=1000)
    image = models.FileField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    fk = models.ForeignKey(User, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    u_page = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_page_blog', null=True)

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    fk = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)



