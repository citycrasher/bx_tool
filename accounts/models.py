from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User_url_report(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    new         = models.IntegerField(default=0)
    duplicate   = models.IntegerField(default=0)
    whitelisted = models.IntegerField(default=0)
    invalid_url = models.IntegerField(default=0)
    meta_new    = models.IntegerField(default=0)
    meta_deplicate = models.IntegerField(default=0)
    meta_invalid = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username