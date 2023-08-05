from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Client(models.Model):
    client_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.client_name

class youtube_whitelist(models.Model):
    channel_title = models.CharField(max_length=30)
    channel_id    = models.CharField(max_length=30, unique=True)
    channel_url   = models.CharField(max_length=1500, unique=True)
    client        = models.ForeignKey(Client, on_delete=models.CASCADE)
    added_by      = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.channel_title

class Youtube_Url_Model(models.Model):
    channel_url   = models.CharField(max_length=1500, null=True)
    upload_date = models.CharField(max_length=30, null=True)
    channel_name = models.CharField(max_length=30, null=True)
    content_title = models.CharField(max_length=1500, null=True)
    views = models.IntegerField(default=0, null=True)
    content_duration = models.CharField(max_length=10, default=0, null=True)
    channel_sub_count = models.IntegerField(default=0, null=True)
    video_url = models.CharField(max_length=50, unique=True)
    added_by  = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.video_url

class User_url_report(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    new         = models.IntegerField(default=0)
    duplicate   = models.IntegerField(default=0)
    whitelisted = models.IntegerField(default=0)
    invalid_url = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username