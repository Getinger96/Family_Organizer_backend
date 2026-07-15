from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        PARENT = 'parent', 'Parent'
        CHILD = 'child', 'Child'
     
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PARENT)

    def __str__(self):
        return self.username
    
    

class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    age = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='child_images/', blank=True, null=True)
    password  = models.CharField(max_length=8, default="")
    def __str__(self):
        return f"{self.name} - Child of {self.parent.username}"