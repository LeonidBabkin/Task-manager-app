from django.test import TestCase, Client
from django.utils.translation import gettext_lazy as tr
from task_manager.users.models import NewUser
from django.urls import reverse
from task_manager.utils import remove_rollbar


@remove_rollbar
class HomeTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()


class TestHomePage(HomeTestCase):

    def test_open(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_context(self):
        resp = self.client.get('')
        self.assertContains(resp, tr('Менеджер задач'), status_code=200)
        self.assertTemplateUsed(resp, 'index.html')


class NewUserModelTest(HomeTestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        NewUser.objects.create(first_name='Bob', last_name='Big')

    def test_first_name_label(self):
        author = NewUser.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'имя')

    def test_first_name_max_length(self):
        author = NewUser.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_last_name_comma_first_name(self):
        author = NewUser.objects.get(id=1)
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
