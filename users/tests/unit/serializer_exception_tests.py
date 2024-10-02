import uuid
from django.test import TestCase, override_settings
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from graphql import GraphQLError

from users.models import UserModel
from users.tests.factory import UserFactory
from users.serializers import (
	CreateSerializedUser,
	CreateSerializedUsers,
	UpdateSerializedUser,
	UpdateSerializedUsers
)


@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class SerilizerExceptionTestCase(TestCase):
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

    def test_create_serialized_user_handles_exception(self):
        self.user = UserFactory(username='JDog')
        user_data = self.create_user_data()

        try:
            CreateSerializedUser(user_data).is_valid()
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, 'User input is not valid')
        self.assertEqual(error_response.extensions['code'], 'ValidationError')
        self.assertEqual(error_response.extensions['original_error'], "{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}")
        self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
        self.assertEqual(error_response.extensions['function_name'], 'create_record')

    def test_update_record_handles_exception(self):
        self.user = UserFactory(username='JDog')
        user_record = UserFactory()
        user_record.username = self.user.username
        user_data = self.create_user_data(user_record.id)

        try:
            UpdateSerializedUser(user_data).is_valid()
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, 'User input is not valid')
        self.assertEqual(error_response.extensions['code'], 'ValidationError')
        self.assertEqual(error_response.extensions['original_error'], "{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}")
        self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
        self.assertEqual(error_response.extensions['function_name'], 'update_record')
