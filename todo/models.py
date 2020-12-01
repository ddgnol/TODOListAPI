

from django.db import models


# Create your models here.
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    objects = models.Manager()
    owner = models.ForeignKey('users.User', related_name='task', on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.ForeignKey('users.User', related_name='task_member', on_delete=models.CASCADE)
    task = models.ForeignKey('todo.Task', related_name='task', on_delete=models.CASCADE)
    role = models.IntegerField(default=2)
    objects = models.Manager()

    def __str__(self):
        return self.task.title + self.user.username
