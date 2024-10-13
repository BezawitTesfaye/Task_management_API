
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

class CustomUser(AbstractUser):
    tasks = models.ManyToManyField('Task', related_name='users')
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)