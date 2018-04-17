from django.db import models

# Create your models here.


class HotInfo(models.Model):
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
