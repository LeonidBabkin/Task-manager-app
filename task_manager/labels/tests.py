from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from task_manager.users.models import NewUser
from task_manager.utils import remove_rollbar


@remove_rollbar
class TestLabel(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_label(self):
        self.client.login()
        new_label = {
            'name': 'Bug',
        }
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 200)
        label = Label.objects.last()
        self.assertFalse(label == 'Bug')
        self.client.post(reverse_lazy('label_create'), new_label, follow=True)
        new_label = Label.objects.last()
        self.assertTrue(new_label.name == 'Bug')

    def test_update_label(self):
        update_label = Label.objects.last()
        auth_user = NewUser.objects.last()
        response = self.client.get(reverse_lazy('label_update', args=(update_label.id,)))
        self.client.force_login(auth_user)
        response = self.client.get(reverse_lazy('label_update', args=(update_label.id,)))
        self.assertEqual(response.status_code, 200)
        new_label = {
            'name': 'Bug resolved',
        }
        label = Label.objects.last()
        self.assertFalse(label == 'Bug resolved')
        response = self.client.post(
            reverse_lazy('label_update', args=(update_label.id,)),
            new_label,
            follow=True
        )
        new_label = Label.objects.last()
        self.assertTrue(new_label.name == 'Bug resolved')

    def test_delete_label(self):
        self.client.login()
        delete_label = Label.objects.last()
        response = self.client.get(reverse_lazy('label_delete', args=(delete_label.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('label_delete', args=(delete_label.id,)),
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), "Метка успешно удалена")
        label = Label.objects.last()
        self.assertTrue(label.name == 'Имя метки')
