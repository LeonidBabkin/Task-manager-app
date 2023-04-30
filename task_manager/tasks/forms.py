from django import forms
from django.utils.translation import gettext as tr
from task_manager.tasks.models import Task
from task_manager.statuses.models import TaskStatus
from task_manager.users.models import NewUser



class ShowTasksForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = tr("__all__",)
        exclude = ('created_at', 'name', 'description', 'author')
 
class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('created_at',)  # take all the fileds from the model Task
        fields = tr("__all__",)  # with excluded 'created_at' filed
