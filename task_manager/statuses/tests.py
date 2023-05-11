from django.urls import reverse_lazy
from django.test import TestCase
from task_manager.utils import remove_rollbar
from task_manager.statuses.models import TaskStatus


@remove_rollbar
class TestStatusesList(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    def test_statuses_view(self):
        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='statuses.html'
        )

    def test_statuses_content(self):
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(len(response.context['statuses']), TaskStatus.objects.count())
        self.assertQuerysetEqual(
            response.context['statuses'],
            TaskStatus.objects.all(),
            ordered=False
        )

    def test_statuses_links(self):
        response = self.client.get(reverse_lazy('statuses'))
        self.assertContains(response, '/statuses/create/')
        for pk in range(1, TaskStatus.objects.count() + 1):
            self.assertContains(response, f'/statuses/{pk}/update/')
            self.assertContains(response, f'/statuses/{pk}/delete/')

    def test_statuses_not_logged_in_view(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 200)


@remove_rollbar
class TestCreateStatus(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    def test_create_status(self):
        self.client.login()
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/create_status.html')

        new_status = {
            'name': 'New Status',
        }
        response = self.client.get(reverse_lazy('status_create'))
 
        self.assertEqual(response.status_code, 200)
        last_status = TaskStatus.objects.last()
        self.assertFalse(last_status.name == 'New Status')
        response = self.client.post(reverse_lazy('status_create'), new_status, follow=True)
        new_status = TaskStatus.objects.last()
        self.assertTrue(new_status.name == 'New Status')

    def test_create_status_not_loggedin(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)


@remove_rollbar
class TestUpdateStatus(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    def test_update_status(self):
        self.client.login()
        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/update_status.html')

        update_status = TaskStatus.objects.get(pk=1)
        new_status = {
            'name': 'Almost finished off',
        }
        response = self.client.post(
            reverse_lazy('status_update', 
                         args=(update_status.id,)),
                         new_status,
                         follow=True)
        new_status = TaskStatus.objects.get(pk=1)
        self.assertTrue(new_status.name == 'Almost finished off')

    def test_update_not_logged_in_view(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 200)


@remove_rollbar
class TestDeleteStatusView(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_delete_status_logged_in(self):
        self.client.login()
        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete_status.html')

    def test_delete_status_not_logged_in_view(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)