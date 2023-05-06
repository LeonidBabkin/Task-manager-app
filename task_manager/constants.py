from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


ERROR_URL = reverse_lazy('login')
ERROR_MESSAGE = _('You are not logged in! Please, log in.')