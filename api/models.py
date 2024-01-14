from django.db import models
from jsonfield import JSONField
from django_resized import ResizedImageField
import moviepy.editor as moviepy

class User(models.Model):
  name = models.CharField(max_length=30)
  password = models.CharField(max_length=30)
  avatar = ResizedImageField(blank=True, size=[500, 500], force_format='WEBP', quality=1, upload_to='api/media/avatars/')
  subscribers = models.JSONField(blank=True, null=True, default="[]")
  subscriptions = models.JSONField(blank=True, null=True, default="[]")
  posts = models.JSONField(blank=True, null=True, default="[]")


class MediaImages(models.Model):
  media = ResizedImageField(quality=100, force_format='WEBP', upload_to='api/media/images/')

class MediaVideos(models.Model):
  media = models.FileField(upload_to='api/media/videos/')
