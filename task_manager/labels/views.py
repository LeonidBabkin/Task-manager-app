from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as tr
from task_manager.labels.forms import CreateLabelForm, ShowLabelsForm
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.users.models import NewUser
from django.urls import reverse_lazy
from django.contrib import messages


class LabelsView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = ShowLabelsForm()
        context = {
                'labels': Label.objects.all().order_by('id'),
                'form': form
            }
        return render(request, 'labels.html', context)
    

class LabelCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        form = CreateLabelForm()
        return render(request, 'labels/create_label.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateLabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Метка успешно создана'))
            return redirect('home')
        else:
            return render(request, 'labels/create_label.html', {'form': form})
