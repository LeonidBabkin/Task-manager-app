from django.views.generic import TemplateView, DeleteView
from django.utils.translation import gettext_lazy as tr
from django.shortcuts import render, redirect
from task_manager.tasks.models import Task
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from . import forms
from . import models


class Index(TemplateView):

    template_name = 'index.html'


class UserRegisterView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        form = forms.CreateUserForm()
        context['registration_form'] = form
        return render(request, 'users/register.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():  # Если данные корректные, то сохраняем данные формы
            form.save()
            messages.success(request, "Пользователь зарегистрирован")
            return redirect(reverse_lazy('login'))  # Редирект на указанный маршрут
        messages.error(request, 'Ошибка в регистрации. Попробуйте снова')
        context['registration_form'] = form
        return render(request, 'users/register.html', context)


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        current_user = request.user  # take a logged in user
        user_id = kwargs.get('pk')  # take the pk of a user passed on from the users.html as user.id
        if current_user.id == user_id:  # to update logged in and chosen users must coincide
            user = models.NewUser.objects.get(id=user_id)  # retrieve the user from the DB
            form = forms.CreateUserForm(instance=user)  # give out a form with user's data filled in
            return render(request, 'users/update_user.html', {'form': form})
        else:
            messages.error(request, tr(
                'У вас нет прав для изменения другого пользователя.'))
            return redirect('users')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')  # take the pk of a user passed on from the users.html as user.id
        user = models.NewUser.objects.get(id=user_id)  # retrieve the user from the DB
        form = forms.CreateUserForm(request.POST, instance=user)  # fill out the form with user's
        if form.is_valid():                                       # credentials
            form.save()
            messages.info(request, tr('Пользователь успешно изменён'))
            return redirect('users')
        else:
            return render(request, 'users/update_user.html', {'form': form})


class UserDeleteView(DeleteView):

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get('pk')
        if current_user.id == user_id:
            user = models.NewUser.objects.get(id=user_id)
            return render(request, 'users/delete_user.html', {'user': user})
        else:
            messages.error(request, tr(
                'У вас нет прав для изменения другого пользователя.'))
            return redirect('users')

    def post(self, request, *args, **kwargs):
        current_user = request.user
        user_id = kwargs.get('pk')
        if current_user.id == user_id and not Task.objects.filter(author_id=request.user.pk):
            user = models.NewUser.objects.get(id=user_id)
            logout(request)
            user.delete()
            messages.info(request, tr('Пользователь успешно удалён'))
            return redirect('users')
        else:
            messages.error(request, tr('Невозможно удалить пользователя ',
                                       'потому что он используется'))
            return redirect('users')
