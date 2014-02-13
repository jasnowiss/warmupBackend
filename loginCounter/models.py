import datetime
from django.db import models

# Create your models here.
class Users(models.Model):
    uid = models.CharField(max_length=128) # username
    pid = models.CharField(max_length=128) # password
    count = models.IntegerField(default=1) # counter

