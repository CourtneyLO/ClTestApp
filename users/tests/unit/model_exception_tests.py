from django.test import TestCase
from graphql import GraphQLError

from users.models import UserModel


class UserModelExceptionTestCase(TestCase):
    def test_model_by_name_handles_exception_when_name_does_not_exist(self):
        try:
            UserModel.by_name('Freddy', accepts_does_not_exist=False)
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, 'User record does not exist')
        self.assertEqual(error_response.extensions['code'], 'NOT_FOUND')
        self.assertEqual(error_response.extensions['original_error'], 'UserModel matching query does not exist.')
        self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
        self.assertEqual(error_response.extensions['function_name'], 'get_record_by_name')

    def test_model_by_username_handles_exception_when_user_name_does_not_exist(self):
        try:
            UserModel.by_username('Freddy', accepts_does_not_exist=False)
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, 'User record does not exist')
        self.assertEqual(error_response.extensions['code'], 'NOT_FOUND')
        self.assertEqual(error_response.extensions['original_error'], 'UserModel matching query does not exist.')
        self.assertEqual(error_response.extensions['model_or_class'], 'UserModel')
        self.assertEqual(error_response.extensions['function_name'], 'get_record_by_username')
