from django import forms
from django.utils.translation import gettext as tr
from task_manager.tasks.models import Task
from task_manager.statuses.models import TaskStatus
from task_manager.users.models import NewUser
from task_manager.labels.models import Label


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        # exclude = ('created_at', 'author')  # take all the fileds from the model Task
        # fields = tr("__all__",)  # with excluded 'created_at' filed
        fields = ['name', 'description', 'status', 'executor', 'labels']

class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('created_at', 'author')
        fields = tr("__all__",)