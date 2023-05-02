from django import forms
from django.utils.translation import gettext as tr
from task_manager.labels.models import Label
from task_manager.statuses.models import TaskStatus
from task_manager.users.models import NewUser


class ShowLabelsForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = tr("__all__",)


class CreateLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        exclude = ('created_at',)  # take all the fileds from the model Task
        fields = tr("__all__",)  # with excluded 'created_at' filed
