from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AppConfig(models.Model):
    company_name = models.CharField(max_length=30, unique=True)
    company_address = models.CharField(max_length=250)
    company_legal_email = models.CharField(max_length=50)
    ip_reporting_template = models.TextField()
    Environment_CHOICES = [
        ('PROD', 'Production'),
        ('DEV', 'Development'),
    ]

    environment = models.CharField(max_length=10, choices=Environment_CHOICES, default='DEV')
    def __str__(self):
        return self.company_name

class Services(models.Model):
    services_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.services_name

class Client(models.Model):
    client_name = models.CharField(max_length=30, unique=True)
    services = models.ManyToManyField(Services, blank=True)
    client_country = models.CharField(max_length=10)
    def __str__(self):
        return self.client_name


class Movie(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=50)
    original_work = models.TextField()
    email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)  # Set on creation
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.movie_name

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



class IP_Report(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    report_url = models.CharField(max_length=1500, unique=True)
    Report_CHOICES = [
        ('COPYRIGHT', 'Copyright'),
        ('TRADEMARK', 'Trademark')
    ]
    report_type = models.CharField(max_length=10, choices=Report_CHOICES, default='COPYRIGHT')
    original_type = models.CharField(max_length=15,default="") # pic , video
    report_id = models.IntegerField(default=0)
    request_id = models.IntegerField(default=0)
    Status_CHOICES = [
        ('REPORTED', 'Reported'),
        ('PENDING', 'Pending'),
        ('REMOVED', 'Removed'),
    ]
    status = models.CharField(max_length=10, choices=Status_CHOICES, default='PENDING')
    time_stamp = models.DateField(auto_now_add=True)  # Set on creation

    def __str__(self):
        return "{} | {} | {}".format(self.client, self.movie ,self.report_url)

