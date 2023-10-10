from django.db import models 
class User(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField()
    password = models.CharField(max_length=1000)
