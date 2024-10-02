import uuid
from django.test import TestCase, override_settings
from django.db import models
from graphql import GraphQLError

from users.models import UserModel
from users.tests.factory import UserFactory


@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class MainBaseModelExceptionTestCase(TestCase):
	def test_model_by_id(self):
		try:
			UserModel.by_id('aae851e1-0d23-41eb-94d3-ece0d11a6b63')
		except Exception as error:
			error_response = error

		self.assertTrue(isinstance(error_response, GraphQLError))
		self.assertEqual(error_response.message, 'User record does not exist')
		self.assertEqual(error_response.extensions['code'], 'NOT_FOUND')
		self.assertEqual(error_response.extensions['original_error'], 'UserModel matching query does not exist.')
		self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
		self.assertEqual(error_response.extensions['function_name'], 'get_record_by_id')

	def test_delete_record(self):
		try:
			UserModel.delete_record(['aae851e1-0d23-41eb-94d3-ece0d11a6b63'])
		except Exception as error:
			error_response = error

		self.assertTrue(isinstance(error_response, GraphQLError))
		self.assertEqual(error_response.message, 'Record could not be deleted')
		self.assertEqual(error_response.extensions['code'], 'ServerError')
		self.assertEqual(eval(error_response.extensions['original_error']), ["“['aae851e1-0d23-41eb-94d3-ece0d11a6b63']” is not a valid UUID."])
		self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
		self.assertEqual(error_response.extensions['function_name'], 'delete_record')

	def test_delete_multiple_records(self):
		user = UserFactory.create()

		try:
			UserModel.delete_records('aae851e1-0d23-41eb-94d3-ece0d11a6b63')
		except Exception as error:
			error_response = error

		self.assertTrue(isinstance(error_response, GraphQLError))
		self.assertEqual(error_response.message, 'Records could not be deleted')
		self.assertEqual(error_response.extensions['code'], 'ServerError')
		self.assertEqual(error_response.extensions['original_error'], "['“a” is not a valid UUID.']")
		self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
		self.assertEqual(error_response.extensions['function_name'], 'delete_records')

		records = UserModel.objects.all()
		self.assertEqual(len(records), 1)
