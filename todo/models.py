from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    objects = models.Manager()
    owner = models.ForeignKey('users.User', related_name='task', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
