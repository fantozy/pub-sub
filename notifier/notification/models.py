from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=500)