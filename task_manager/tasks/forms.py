from django import forms
from django.utils.translation import gettext as tr
from task_manager.tasks.models import Task
from task_manager.tasks.models import Label
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter

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


class TasksFilterForm(FilterSet):

    labels = ModelChoiceFilter(field_name='label', label=tr('Метка'),
                               queryset=Label.objects.all().order_by('pk'),
                               )
    self_tasks = BooleanFilter(
        label=tr('Только свои задачи'),
        widget=forms.CheckboxInput(),
        method='only_self'
    )

    def only_self(self, queryset, name, value):
        result = queryset.filter(author=self.request.user).order_by('pk')
        if value:
            return result.order_by('pk')
        return queryset.order_by('pk')

    class Meta:
        model = Task
        fields = ['status', 'executor']