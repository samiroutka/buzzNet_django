from django.db import models
from jsonfield import JSONField
from django_resized import ResizedImageField

class User(models.Model):
  name = models.CharField(max_length=30)
  password = models.CharField(max_length=30)
  avatar = ResizedImageField(blank=True, size=[500, 500], force_format='WEBP', quality=1, upload_to='api/media/')
  subscribers = models.JSONField(blank=True, null=True, default="[]")
  subscriptions = models.JSONField(blank=True, null=True, default="[]")
  posts = models.JSONField(blank=True, null=True, default="[]")
