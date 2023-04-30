from task_manager.statuses.forms import CreateStatusForm, UpdateStatusForm
from django.utils.translation import gettext_lazy as tr
from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView
)
from task_manager.statuses.models import TaskStatus
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.contrib import messages


class StatusesView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name='statuses.html',
            context={
                'statuses': TaskStatus.objects.all().order_by('id'),
                'title': 'Statuses'
            }
        )


class StatusCreationView(CreateView):

    def get(self, request, *args, **kwargs):
        form = CreateStatusForm()
        return render(request, 'statuses/create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Статус успешно создан'))
            return redirect(reverse_lazy('statuses'))
        else:
            return render(request, 'statuses/create_status.html', {'form': form})


class StatusUpdateView(UpdateView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = TaskStatus.objects.get(id=status_id)
        form = UpdateStatusForm(instance=status)
        return render(request, 'statuses/update_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = TaskStatus.objects.get(id=status_id)
        form = UpdateStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Статус успешно изменён'))
            return redirect('statuses')
        else:
            return render(request, 'statuses/update_status.html', {'form': form})


class StatusDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        context = {}
        status = TaskStatus.objects.get(id=status_id)
        context['status'] = status
        return render(request, 'statuses/delete_status.html', context)

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        context = {}
        status = TaskStatus.objects.get(id=status_id)  # retrieve a status from db
        if Task.objects.filter(status=status):
            messages.error(
                self.request,
                tr('Невозможно удалить статус, потому что он используется')
            )
            return redirect('statuses')
        context['status'] = status
        status.delete()
        messages.info(request, tr('Статус успешно удалён'))
        return redirect('statuses')