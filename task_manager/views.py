from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as tr
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from task_manager.users.models import NewUser
from . import forms


class Index(TemplateView):
        template_name = 'index.html'


class UserLoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = {}
        form = forms.LoginUserForm()
        context['login_form'] = form
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = forms.LoginUserForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.info(request, tr('Вы залогинены'))
                return redirect('home')
        messages.error(request, tr(
            'Пожалуйста, введите правильные имя пользователя и пароль. '
            'Оба поля могут быть чувствительны к регистру.')
        )

        context['login_form'] = form
        # print(context['login_form']['password'].errors)
        return render(request, 'login.html', context)


class UserLogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        messages.info(request, tr('Вы разлогинены'))
        logout(request)
        return redirect('home')


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name='users.html',
            context={
                'users': NewUser.objects.all().order_by('id'),
                'title': 'Users'
            }
        )
