from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as tr


class Label(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = tr('Метка')
        verbose_name_plural =tr('Метки')

    def __str__(self):
        return self.name
