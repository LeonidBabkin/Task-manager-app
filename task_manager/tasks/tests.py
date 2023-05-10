from django.test import TestCase
from django.urls import reverse

# from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.users.models import NewUser


class TaskTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_task(self):
        new_task = {
            'name': 'Task',
            'description': 'Task in process',
            'status': 2,
            'labels': [2],
            'executor': 1
        }
        response = self.client.get(reverse('task_create'))
        self.assertRedirects(response, reverse('login'), 302)
        auth_user = NewUser.objects.last()
        self.client.force_login(auth_user)
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 12)
        response = self.client.post(
            reverse('task_create'),
            new_task,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks'), 302)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 13)
        task = Task.objects.last()
        self.assertTrue(task.name == 'Task')
        self.assertTrue(task.description == 'Task in process')
        self.assertTrue(task.status.name == "Завершился с ошибкой.")
        self.assertTrue(task.executor.username == 'LevRus')
        self.assertTrue(task.author.username == auth_user.username)
        self.assertFalse(task.labels.count(), 3)
