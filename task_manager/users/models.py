from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class NewUser(AbstractUser):
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()
