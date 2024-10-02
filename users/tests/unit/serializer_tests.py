import uuid
from django.test import TestCase, override_settings
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import UserModel
from users.tests.factory import UserFactory
from users.serializers import (
	CreateSerializedUser,
	CreateSerializedUsers,
	UpdateSerializedUser,
	UpdateSerializedUsers
)


@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class SerilizerTestCase(TestCase):
        def create_user_data(self, id=None):
            user_data = {
                'name': 'John',
                'username': 'JDog',
                'profile_picture': SimpleUploadedFile("test_image.jpg", b"hello")
            }

            if id:
                user_data['id'] = id

            return user_data

        def create_second_user_data(self, id=None):
            user_data = {
                'name': 'Adam',
                'username': 'Mada',
                'profile_picture': SimpleUploadedFile("test_image.jpg", b"hello")
            }

            if id:
                user_data['id'] = id

            return user_data

        def is_valid_uuid(self, id):
            try:
                uuid.UUID(str(id))
                return True
            except ValueError:
            	return False

        def test_create_serialized_user(self):
            user_data = self.create_user_data()

            # Add Serilizered Data to the Database
            user = CreateSerializedUser(user_data).is_valid()

            # Check Response is Correct
            self.assertEqual(user.name, 'John')
            self.assertEqual(user.username, 'JDog')
            self.assertEqual(user.profile_picture, f'{user.id}/profile')

            # Check Data is Saved in the Database
            records = UserModel.objects.all()
            self.assertEqual(len(records), 1)
            self.assertTrue(self.is_valid_uuid(records[0].id))
            self.assertEqual(records[0].name, 'John')
            self.assertEqual(records[0].username, 'JDog')
            self.assertEqual(records[0].profile_picture, f'{records[0].id}/profile')

        def test_create_multiple_records(self):
            user_data_1 = self.create_user_data()
            user_data_2 = self.create_second_user_data()

            # Add Serilizered Data to the Database
            [user_1, user_2] = CreateSerializedUsers([user_data_1, user_data_2]).is_valid()

            # Check Response is Correct
            self.assertEqual(user_1.name, 'John')
            self.assertEqual(user_1.username, 'JDog')
            self.assertEqual(user_1.profile_picture, f'{user_1.id}/profile')

            self.assertEqual(user_2.name, 'Adam')
            self.assertEqual(user_2.username, 'Mada')
            self.assertEqual(user_2.profile_picture, f'{user_2.id}/profile')

            # Check Data is Saved in the Database
            records = UserModel.objects.all()
            self.assertEqual(len(records), 2)
            self.assertTrue(self.is_valid_uuid(records[0].id))
            self.assertEqual(records[0].name, 'Adam')
            self.assertEqual(records[0].username, 'Mada')
            self.assertEqual(records[0].profile_picture, f'{records[0].id}/profile')
            self.assertTrue(self.is_valid_uuid(records[1].id))
            self.assertEqual(records[1].name, 'John')
            self.assertEqual(records[1].username, 'JDog')
            self.assertEqual(records[1].profile_picture, f'{records[1].id}/profile')

        def test_update_record(self):
            user_record = UserFactory()

            # Check Data is Correctly Added
            records = UserModel.objects.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].id, user_record.id)
            self.assertEqual(records[0].name, user_record.name)
            self.assertEqual(records[0].username, user_record.username)

            # Get New Data to Change Existing Data
            user_data = self.create_user_data(user_record.id)

            # Update Serilizered Data in the Database
            user = UpdateSerializedUser(user_data).is_valid()

            # Check Response is Correct
            self.assertEqual(user.name, 'John')
            self.assertEqual(user.username, 'JDog')
            self.assertEqual(user.profile_picture, f'{user.id}/profile')

            # Check Data is Saved in the Database
            records = UserModel.objects.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].id, user_record.id)
            self.assertEqual(records[0].name, 'John')
            self.assertEqual(records[0].username, 'JDog')
            self.assertEqual(records[0].profile_picture, f'{user_record.id}/profile')

        def test_update_multiple_records(self):
            user_record_1 = UserFactory.create()
            user_record_2 = UserFactory.create()

            # Check Data is Correctly Added
            records = UserModel.objects.all()
            self.assertEqual(len(records), 2)

            record_1 = UserModel.objects.get(pk=user_record_1.id)
            self.assertEqual(record_1.id, user_record_1.id)
            self.assertEqual(record_1.name, user_record_1.name)
            self.assertEqual(record_1.username, user_record_1.username)

            record_2 = UserModel.objects.get(pk=user_record_2.id)
            self.assertEqual(record_2.id, user_record_2.id)
            self.assertEqual(record_2.name, user_record_2.name)
            self.assertEqual(record_2.username, user_record_2.username)

            # Get New Data to Change Existing Data
            user_data_1 = self.create_user_data(user_record_1.id)
            user_data_2 = self.create_second_user_data(user_record_2.id)

            # Update Serilizered Data in the Database
            [user_1, user_2] = UpdateSerializedUsers([user_data_1, user_data_2]).is_valid()

            # Check Response is Correct
            self.assertEqual(user_1.name, 'John')
            self.assertEqual(user_1.username, 'JDog')
            self.assertEqual(user_1.profile_picture, f'{user_1.id}/profile')

            self.assertEqual(user_2.name, 'Adam')
            self.assertEqual(user_2.username, 'Mada')
            self.assertEqual(user_2.profile_picture, f'{user_2.id}/profile')

            # Check Data is Saved in the Database
            records = UserModel.objects.all()
            self.assertEqual(len(records), 2)

            record_1 = UserModel.objects.get(pk=user_record_1.id)
            self.assertEqual(record_1.id, user_data_1['id'])
            self.assertEqual(record_1.name, 'John')
            self.assertEqual(record_1.username, 'JDog')
            self.assertEqual(record_1.profile_picture, f'{user_data_1['id']}/profile')

            record_2 = UserModel.objects.get(pk=user_record_2.id)
            self.assertEqual(record_2.id, user_data_2['id'])
            self.assertEqual(record_2.name, 'Adam')
            self.assertEqual(record_2.username, 'Mada')
            self.assertEqual(record_2.profile_picture, f'{user_data_2['id']}/profile')
