from django.test import TestCase
from django.utils.translation import gettext_lazy as tr
from task_manager.users.models import NewUser


class TestHomePage(TestCase):

    def test_open(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_context(self):
        resp = self.client.get('')
        self.assertContains(resp, tr('Менеджер задач'), status_code=200)
        self.assertTemplateUsed(resp, 'index.html')


class NewUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        NewUser.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = NewUser.objects.get(id=1)
        print('first')
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        author = NewUser.objects.get(id=1)
        print('second')
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_last_name_comma_first_name(self):
        author = NewUser.objects.get(id=1)
        print('third')
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)
