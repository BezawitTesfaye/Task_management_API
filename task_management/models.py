
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    class Meta:
        app_label = 'task_management'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

class CustomUser(AbstractUser):
    tasks = models.ManyToManyField('Task', related_name='users')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )
CustomUser.groups.field.remote_field.related_name = 'custom_user_groups'
CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_permissions'
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    due_date = models.DateField(null=True, blank=True)

    def mark_as_complete(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()

    def mark_as_incomplete(self):
        if self.completed:
            self.completed = False
            self.completed_at = None
            self.save()

  