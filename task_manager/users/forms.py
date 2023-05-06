from django.utils.translation import gettext as tr
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser
from django import forms


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(label=tr('Имя'),
                                 label_suffix='',
                                 max_length=100,
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': tr('Имя'),
                                            'class': 'form-control', }))
    last_name = forms.CharField(label=tr('Фамилия'),
                                label_suffix='',
                                max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': tr('Фамилия'),
                                           'class': 'form-control', }))
    username = forms.CharField(label=tr('Имя пользователя'),
                               max_length=20,
                               label_suffix='',
                               required=True,
                               help_text=tr('Обязательное поле. '
                                            'Не более 150 символов. '
                                            'Только буквы, цифры и символы @/./+/-/_.'),
                               widget=forms.TextInput(
        attrs={'placeholder': tr('Имя пользователя'),
               'autofocus': True,
               'class': 'form-control', }),
        error_messages={'unique': tr('Пользователь с таким именем '
                                     'уже есть')})
    password1 = forms.CharField(label=tr('Пароль'),
                                label_suffix='',
                                max_length=100,
                                required=True,
                                help_text=tr(
                                "Ваш пароль должен содержать "
                                "как минимум 3 символа."),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': tr('Пароль'),
                                           'class': 'form-control', }))
    password2 = forms.CharField(label=tr('Подтверждение пароля'),
                                label_suffix='',
                                max_length=100,
                                required=True,
                                help_text=tr("Для подтверждения введите,"
                                             " пожалуйста, пароль ещё раз."),
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': tr('Подтверждение '
                                                          'пароля'),
                                        'class': 'form-control', }))

    class Meta:
        model = NewUser
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )
