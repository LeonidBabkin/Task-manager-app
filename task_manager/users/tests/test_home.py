from django.test import TestCase, Client
from task_manager.users.models import NewUser
from django.urls import reverse
from task_manager.utils import remove_rollbar
from django.urls import reverse_lazy
from django.utils.translation import gettext as tr


@remove_rollbar
class HomeTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'test_user',
            'password': 'te$t_pa$$word',
            'first_name': 'Bob',
            'last_name': 'Big'
        }
        self.user = NewUser.objects.create_user(**self.credentials)
        # print(self.user.id)


class TestHomePage(HomeTestCase):

    def test_open(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_context(self):
        resp = self.client.get('')
        self.assertContains(resp, tr('Менеджер задач'), status_code=200)
        self.assertTemplateUsed(resp, 'index.html')


class TestUserCredentials(HomeTestCase):

    def test_first_name_label(self):
        author = NewUser.objects.filter(first_name='Bob').last()
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'имя')

    def test_first_name_max_length(self):
        author = NewUser.objects.filter(first_name='Bob').last()
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_last_name_comma_first_name(self):
        author = NewUser.objects.filter(first_name='Bob').last()
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEqual(str(author), expected_object_name)


class UserTest(HomeTestCase):

    def test_create_user(self):
        new_user = {
            'first_name': 'Ivan',
            'last_name': 'Sidarov',
            'username': 'Ivan_Sidarov',
            'password1': 'Rucyh2UTJrWUD2Akwo6victory',
            'password2': 'Rucyh2UTJrWUD2Akwo6victory'
        }
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(NewUser.objects.filter(username=new_user['username']))
        response = self.client.post(
            reverse('register'),
            new_user,
            follow=True
        )
        self.assertRedirects(response, reverse('login'), 302)
        new_user = NewUser.objects.last()  # last in the DB
        self.assertTrue(new_user.username == 'Ivan_Sidarov')
        self.assertTrue(new_user.check_password('Rucyh2UTJrWUD2Akwo6victory'))
        self.assertTrue(new_user.first_name == 'Ivan')
        self.assertTrue(new_user.last_name == 'Sidarov')

    def test_update_user(self):
        update_user = NewUser.objects.last()
        self.client.force_login(update_user)
        response = self.client.get(reverse('user_update', args=(update_user.id,)))
        self.assertEqual(response.status_code, 200)
        new_user = {
            'first_name': 'Leo',
            'last_name': 'Bab',
            'username': 'LeoBab',
            'password1': 'cyh2UTJrjexWUD2Akwo6',
            'password2': 'cyh2UTJrjexWUD2Akwo6'
        }
        self.assertFalse(NewUser.objects.filter(username=new_user['username']))
        response = self.client.post(
            reverse('user_update', args=(update_user.id,)),
            new_user,
            follow=True)
        self.assertRedirects(response, reverse('users'), 302)
        new_user = NewUser.objects.last()
        self.assertTrue(new_user.username == 'LeoBab')
        self.assertTrue(new_user.check_password('cyh2UTJrjexWUD2Akwo6'))
        self.assertTrue(new_user.first_name == 'Leo')
        self.assertTrue(new_user.last_name == 'Bab')

    def test_delete_user(self):
        delete_user = NewUser.objects.last()
        self.assertFalse(delete_user.username == 'Kozma_Prutkov')
        self.client.force_login(delete_user)
        response = self.client.get(reverse('user_delete', args=(delete_user.id,)))
        response = self.client.post(
            reverse('user_delete', args=(delete_user.id,)),
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            "Пользователь успешно удалён"
        )


class HomePageTestCase(HomeTestCase):

    def test_index_view(self):
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')
        self.assertContains(response, tr('Менеджер задач'), status_code=200)

    def test_header_links_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('home'))

        self.assertContains(response, '/users/')
        self.assertContains(response, '/statuses/')
        self.assertContains(response, '/labels/')
        self.assertContains(response, '/tasks/')
        self.assertContains(response, '/logout/')
        self.assertNotContains(response, '/login/')

    def test_header_links_not_logged_in(self):
        response = self.client.get(reverse_lazy('home'))

        self.assertContains(response, '/users/')
        self.assertContains(response, '/login/')
        self.assertContains(response, '/users/create/')
        self.assertNotContains(response, '/statuses/')
        self.assertNotContains(response, '/labels/')
        self.assertNotContains(response, '/tasks/')
        self.assertNotContains(response, '/logout/')


class TestLoginUser(HomeTestCase):
    def test_user_login_view(self):
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')

    def test_user_login(self):
        response = self.client.post(
            reverse_lazy('login'),
            self.credentials,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertTrue(response.context['user'].is_authenticated)


class TestLogoutUser(HomeTestCase):
    def test_user_logout(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse_lazy('logout'),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertFalse(response.context['user'].is_authenticated)
