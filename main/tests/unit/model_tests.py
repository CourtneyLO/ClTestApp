import uuid
from django.test import TestCase, override_settings
from django.db import models

from users.models import UserModel
from users.tests.factory import UserFactory


@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class MainBaseModelExceptionTestCase(TestCase):
	def setUp(self):
		self.user_record = UserFactory()

	def test_model_by_id(self):
		record = UserModel.by_id(self.user_record.id)

		self.assertEqual(record.id, self.user_record.id)
		self.assertEqual(record.name, self.user_record.name)

	def test_model_by_id_accepts_does_not_exist(self):
		record = UserModel.by_id('aae851e1-0d23-41eb-94d3-ece0d11a6b63', True)

		self.assertIsNone(record)

	def test_delete_record(self):
		records = UserModel.objects.all()
		self.assertEqual(len(records), 1)

		UserModel.delete_record(self.user_record.id)

		records = UserModel.objects.all()
		self.assertEqual(len(records), 0)

	def test_delete_record_does_not_return_exception_if_id_does_not_exist(self):
		result = UserModel.delete_record('aae851e1-0d23-41eb-94d3-ece0d11a6b63')
		self.assertIsNone(result)

	def test_delete_multiple_records(self):
		user_record_2 = UserFactory.create()

		records = UserModel.objects.all()
		self.assertEqual(len(records), 2)

		UserModel.delete_records([self.user_record.id, user_record_2.id])

		records = UserModel.objects.all()
		self.assertEqual(len(records), 0)

	def test_delete_records_does_not_return_exception_if_id_does_not_exist(self):
		result = UserModel.delete_records([self.user_record.id, 'aae851e1-0d23-41eb-94d3-ece0d11a6b63'])
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0]['record_id'], self.user_record.id)
		self.assertTrue(result[0]['success'])
