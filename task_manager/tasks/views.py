from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as tr
from task_manager.tasks.forms import CreateTaskForm, UpdateTaskForm
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from task_manager.tasks.forms import TasksFilterForm
from django.urls import reverse


class TasksView(FilterView, LoginRequiredMixin):
    model = Task
    ordering = ['id']
    paginate_by = 10
    filterset_class = TasksFilterForm
    template_name = 'tasks.html'
    context_object_name = "tasks"
    extra_context = {'title': tr('Tasks')}


class TaskCreateView(CreateView, SuccessMessageMixin, LoginRequiredMixin):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')
    # success_message = tr('Задача успешно создана')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, tr('Задача успешно создана'))
        return reverse("tasks")


class TaskUpdateView(UpdateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        form = UpdateTaskForm(instance=task)
        return render(request, 'tasks/update_task.html', {'form': form})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        # put data in the form to edit

        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.info(request, tr('Задача успешно изменена'))
            return redirect('tasks')
        else:
            return render(request, 'tasks/update_task.html', {'form': form})


class TaskDeleteView(DeleteView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):

        # нужно найти user id текущего пользователя и сравнить его с user id автора задачи
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


class TaskDetailView(DetailView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        template_name = 'tasks/detail_task.html'
        task = Task.objects.get(id=task_id)
        extra_context = {'title': tr('Просмотр задачи'), 'task': task}
        return render(request, template_name, extra_context)
