# ip_reporting/models.py
from django.db import models

class CustomPermission(models.Model):
    class Meta:
        permissions = (
            ('can_access_custom_permission', 'Can access custom permission'),
        )

class ApprovedMetaDomain(models.Model):
    approvedDomain = models.TextField(help_text="add domain using (,)")

    def __str__(self):
        return self.approvedDomain