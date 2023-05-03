from typing import Any, Dict
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as tr
from task_manager.tasks.forms import CreateTaskForm, ShowTasksForm, UpdateTaskForm
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.users.models import NewUser
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.filters import TaskFilter


class TasksView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        form = ShowTasksForm()
        context = {
            'form': task_filter.form,
            'tasks': task_filter.qs,
                # 'tasks': Task.objects.all().order_by('id'),
                # 'form': form
            }
        return render(request, 'tasks.html', context)


# class TaskCreateView(CreateView):

#     def get(self, request, *args, **kwargs):
#         form = CreateTaskForm()
#         return render(request, 'tasks/create_task.html', {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = CreateTaskForm(request.POST)
#         if form.is_valid():
# # That's useful when you get most of your model data from a form, but you need to populate 
# # some null=False fields with non-form data.Saving with commit=False gets you a model object, 
# # then you can add your extra data and save it.
#             post = form.save(commit=False)
#             # fill in the field author with with current user id
#             post.author = NewUser.objects.get(id=request.user.id)
#             post.save()
#             messages.info(request, tr('Задача успешно создана'))
#             return redirect('tasks')
#         else:
#             return render(request, 'tasks/create_task.html', {'form': form})
        

class TaskCreateView( LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')
    success_message = tr('Задача успешно создана')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  



class TaskUpdateView(UpdateView):

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

class TaskDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        template_name = 'tasks/detail_task.html'
        task = Task.objects.get(id=task_id)
        extra_context = {'title': tr('Просмотр задачи'), 'task': task,
                     }
        return render(request, template_name, extra_context)
