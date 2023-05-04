from django.db import models
from django.utils import timezone


class TaskStatus(models.Model):
    name = models.CharField(max_length=120, blank=False, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
