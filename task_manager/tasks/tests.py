from django.test import TestCase, Client
from django.urls import reverse_lazy
from task_manager.utils import remove_rollbar
# from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.users.models import NewUser


@remove_rollbar
class TaskTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']

    def test_create_task_view(self) -> None:
        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/create_task.html')


    def test_create_task_not_logged_in_view(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        new_task = {
            'name': 'Task',
            'description': 'Task in process',
            'status': 2,
            'labels': 2,
            'executor': 1
        }
        response = self.client.get(reverse_lazy('task_create'))
        auth_user = NewUser.objects.last()
        self.client.force_login(auth_user)
        response = self.client.get(reverse_lazy('task_create'))
        self.assertTemplateUsed(response, template_name='tasks/create_task.html')
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.count()
        self.assertEqual(tasks, 10)
        response = self.client.post(
            reverse_lazy('task_create'),
            new_task,
            follow=True
        )    
        tasks = Task.objects.count()
        self.assertEqual(tasks, 11)
        task = Task.objects.last()
        self.assertTrue(task.name == 'Task')
        self.assertTrue(task.description == 'Task in process')
        self.assertTrue(task.status.name == "Выполнить asap")
        self.assertTrue(task.executor.username == 'LevRus')
        self.assertTrue(task.author.username == auth_user.username)
        self.assertTrue(task.labels.count(), 1)
        

    def test_update_task(self):
        update_task = Task.objects.last()
        auth_user = NewUser.objects.last()
        response = self.client.get(reverse_lazy('task_update', args=(update_task.id,)))
        self.client.force_login(auth_user)
        response = self.client.get(reverse_lazy('task_update', args=(update_task.id,)))
        self.assertEqual(response.status_code, 200)
        new_task = {
            'name': 'Человек',
            'description': 'Это звучит гордо!',
            'status': 3,
            'labels': [1, 3],
            'executor': 3
        }
        response = self.client.post(
            reverse_lazy('task_update', args=(update_task.id,)),
            new_task,
            follow=True
        )
        new_task = Task.objects.last()
        self.assertTrue(new_task.name == 'Человек')
        self.assertTrue(new_task.description == 'Это звучит гордо!')
        self.assertTrue(new_task.status.name == 'Не задерживай добрых и честных людей')
        self.assertTrue(new_task.executor.username == "admin")
        self.assertTrue(new_task.author.username == 'LevRus')
        self.assertEqual(new_task.labels.count(), 2)
        for t in new_task.labels.values():
            self.assertTrue(t['name'] in ['Label 3', 'Готов к полноценной работе.'])


    def test_delete_task(self):
        delete_task = Task.objects.last()
        auth_user = NewUser.objects.get(pk=delete_task.author.id)
        self.client.force_login(auth_user)
        response = self.client.get(reverse_lazy('task_delete', args=(delete_task.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('task_delete', args=(delete_task.id,)),
            follow=True
        )
        tasks = Task.objects.count()
        self.assertEqual(tasks, 9)
        task = Task.objects.last()
        self.assertTrue(task.name == "Лечебный узел обслуживания")
        self.assertTrue(task.description == "Информационная карточка больного.")


@remove_rollbar
class TestDetailedTask(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    def test_detailed_task_view(self):
        detail_task = Task.objects.get(pk=9)
        auth_user = NewUser.objects.get(pk=detail_task.author.id)
        self.client.force_login(auth_user)
        response = self.client.get(
            reverse_lazy('task_detail', kwargs={'pk': 9})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/detail_task.html'
        )

    def test_detailed_task_content(self):
        response = self.client.get(
            reverse_lazy('task_detail', kwargs={'pk': 9})
        )
        self.assertContains(response, '/tasks/9/update/')
        self.assertContains(response, '/tasks/9/delete/')

        self.assertContains(response, "Счастливое настоящее  - это работа над ним самим!")
        self.assertContains(response, "Претворение в жизнь мира и благоденствия в России")
        self.assertContains(response, 1)
        self.assertContains(response, 5)
        self.assertContains(response, 2)

    def test_detailed_task_not_logged_in(self):
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_detail', kwargs={'pk': 9})
        )
        self.assertEqual(response.status_code, 200)


@remove_rollbar
class TestTasksList(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    def test_tasks_view(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks.html'
        )

    def test_tasks_content(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(len(response.context['tasks']), Task.objects.count())
        self.assertQuerysetEqual(
            response.context['tasks'],
            Task.objects.all(),
            ordered=False
        )

    def test_tasks_links(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertContains(response, '/tasks/create/')
        count = Task.objects.count()
        for pk in [5, 6, 7, 9, 22, 30, 35, 52, 54, 71]:
            self.assertContains(response, f'/tasks/{pk}/update/')
            self.assertContains(response, f'/tasks/{pk}/delete/')

    def test_tasks_not_logged_in_view(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)


