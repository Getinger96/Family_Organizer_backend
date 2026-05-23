from django.db import models
from rest_framework import settings

# Create your models here.
class Child (models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name