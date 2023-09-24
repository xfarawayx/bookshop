from django.db import models

# Create your models here.

class User(models.Model):
    unum = models.CharField(max_length=20, primary_key=True)
    uname = models.CharField(max_length=40, unique=True)
    passwd = models.CharField(max_length=40)
    contact = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.unum

class Manager(models.Model):
    mnum = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=40)
    def __str__(self):
        return self.mnum