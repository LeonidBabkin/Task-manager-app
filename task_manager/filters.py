import django_filters
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as tr
from django import forms


class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
        exclude = ['name',]

    labels = django_filters.ModelChoiceFilter(
        label=tr('Label'),
        queryset=Label.objects.all()
    )

    self_tasks = django_filters.BooleanFilter(
        label=tr('Только свои задачи'),
        widget=forms.CheckboxInput(), method='get_queryset'
    )
    # get queryset(data) from the task_filter.form
    def get_queryset(self, queryset, name, value):
        return queryset
