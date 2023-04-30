from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as tr
from task_manager.tasks.forms import CreateTaskForm, ShowTasksForm, UpdateTaskForm
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.contrib import messages


# @method_decorator(login_required, name='dispatch')
class TasksView(TemplateView):

    def get(self, request, *args, **kwargs):
        form = ShowTasksForm()
        context = {
                'tasks': Task.objects.all().order_by('id'),
                'form': form
            }
        return render(request, 'tasks.html', context)


# @method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        form = CreateTaskForm()
        return render(request, 'tasks/create_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Задача успешно создана'))
            return redirect(reverse_lazy('tasks'))
        else:
            return render(request, 'tasks/create_task.html', {'form': form})
        

class TaskUpdateView(UpdateView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        form = UpdateTaskForm(instance=task)
        return render(request, 'tasks/update_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Задача успешно изменена'))
            return redirect('tasks')
        else:
            return render(request, 'tasks/update_task.html', {'form': form})


class TaskDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        #  нужно найти user id текущего пользователя и сравнить его с user id автора задачи
        current_user = request.user
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)  # get this task from DB
        user_id = task.author_id  # get user id of the task author
        if user_id == current_user.id:
            context = {}
            context['task'] = task
            return render(request, 'tasks/delete_task.html', context)
        else:
            messages.error(request, tr('Задачу может удалить только её автор'))
            return redirect('tasks')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)  # retrieve a status from db
        task.delete()
        messages.info(request, tr('Задача успешно удалена'))
        return redirect('tasks')