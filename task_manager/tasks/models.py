from django.db import models
from django.utils import timezone
from task_manager.users.models import NewUser
from task_manager.labels.models import Label
from task_manager.statuses.models import TaskStatus
from django.utils.translation import gettext_lazy as tr


class Task(models.Model):
    name = models.CharField(verbose_name=tr('Имя'), max_length=120, blank=False)
    description = models.TextField(verbose_name=tr('Описание'), max_length=1000, blank=True)
    status = models.ForeignKey(
        TaskStatus,
        related_name='statuses',
        on_delete=models.PROTECT,
        blank=False,
        verbose_name=tr('Статус')
    )
    author = models.ForeignKey(
        NewUser,
        related_name='author',
        on_delete=models.PROTECT,
        verbose_name=tr('Автор')
    )
    executor = models.ForeignKey(
        NewUser,
        related_name='executor',
        on_delete=models.PROTECT,
        verbose_name=tr('Исполнитель'),
        blank=True,
        null=False
    )
    labels = models.ManyToManyField(
        Label,
        related_name='labels',
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        verbose_name=tr('Метки'),
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
