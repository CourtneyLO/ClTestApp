import random
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import UserModel
from users.serializers import CreateSerializedUser
from users.tests.factory import UserFactory

class UserData(object):
	pass

@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class UserTestCase(TestCase):
    def setUp(self):
        random_number = random.randint(0, 100)
        UserFactory(name='Freddy', username=f'Freddy{random_number}')
        UserFactory(name='Amber', username=f'Amber{random_number}')
        UserFactory(name='James', username=f'James{random_number}')
        UserFactory(name='Paul', username=f'Paul{random_number}')
        UserFactory(name='Annabel', username=f'Annabel{random_number}')

        self.random_number = random_number

    def test_records_are_ordered_by_name(self):
        saved_user_data = UserModel.objects.all()
        self.assertEqual(len(saved_user_data), 5)

        self.assertEqual(saved_user_data[0].name, 'Amber')
        self.assertEqual(saved_user_data[1].name, 'Annabel')
        self.assertEqual(saved_user_data[2].name, 'Freddy')
        self.assertEqual(saved_user_data[3].name, 'James')
        self.assertEqual(saved_user_data[4].name, 'Paul')

    def test_records_str_returns_name(self):
        saved_user_data = UserModel.objects.all()
        self.assertEqual(len(saved_user_data), 5)

        self.assertEqual(str(saved_user_data[0]), 'Amber')
        self.assertEqual(str(saved_user_data[1]), 'Annabel')
        self.assertEqual(str(saved_user_data[2]), 'Freddy')
        self.assertEqual(str(saved_user_data[3]), 'James')
        self.assertEqual(str(saved_user_data[4]), 'Paul')

    def test_model_by_name(self):
        record = UserModel.by_name('Freddy')

        self.assertEqual(record.id, record.id)
        self.assertEqual(record.name, record.name)

    def test_model_by_name_accepts_does_not_exist(self):
        record = UserModel.by_name('Fleddy', True)

        self.assertIsNone(record)

    def test_model_by_username(self):
        record = UserModel.by_username(f'Freddy{self.random_number}')

        self.assertEqual(record.id, record.id)
        self.assertEqual(record.username, record.username)

    def test_model_by_username_accepts_does_not_exist(self):
        record = UserModel.by_username('Fleddy', True)

        self.assertIsNone(record)
