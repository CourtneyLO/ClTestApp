from django.test import TestCase
from graphql import GraphQLError

from users.errors import (
    NotFoundError,
    ValidationError,
    ServerError,
    CustomModelError,
    CustomValidationError
)
from users.models import UserModel

class TestModel:
    pass


class ErrorTestCase(TestCase):
    def test_not_found_error(self):
        exception = Exception('Not Found')
        model = TestModel
        function_name = 'update_record'

        query = '''
        query {
            users {
                id
            }
        }
        '''

        not_found_error = NotFoundError(exception, model, function_name)
        not_found_error.extensions['query'] = query

        self.assertEqual(not_found_error.code, 'NOT_FOUND')
        self.assertEqual(not_found_error.original_error, exception)
        self.assertEqual(not_found_error.message, 'User record does not exist')
        self.assertEqual(not_found_error.model_or_class, TestModel)
        self.assertEqual(not_found_error.function_name, 'update_record')
        self.assertEqual(not_found_error.extensions['code'], 'NOT_FOUND')
        self.assertEqual(not_found_error.extensions['original_error'], "Not Found")
        self.assertEqual(not_found_error.extensions['model_or_class'], 'TestModel')
        self.assertEqual(not_found_error.extensions['function_name'], 'update_record')
        self.assertEqual(not_found_error.extensions['query'], query)
        self.assertTrue(isinstance(not_found_error.graphql_error, GraphQLError))

    def test_validation_error(self):
        exception = Exception('Validation Error')
        model = TestModel
        function_name = 'create_record'

        query = '''
        query {
            users {
                id
            }
        }
        '''

        validation_error = ValidationError(exception, model, function_name)
        validation_error.extensions['query'] = query

        self.assertEqual(validation_error.code, 'ValidationError')
        self.assertEqual(validation_error.original_error, exception)
        self.assertEqual(validation_error.message, 'User input is not valid')
        self.assertEqual(validation_error.model_or_class, TestModel)
        self.assertEqual(validation_error.function_name, 'create_record')
        self.assertEqual(validation_error.extensions['code'], 'ValidationError')
        self.assertEqual(validation_error.extensions['original_error'], 'Validation Error')
        self.assertEqual(validation_error.extensions['model_or_class'], 'TestModel')
        self.assertEqual(validation_error.extensions['function_name'], 'create_record')
        self.assertEqual(validation_error.extensions['query'], query)
        self.assertTrue(isinstance(validation_error.graphql_error, GraphQLError))

    def test_server_error(self):
        exception = Exception('Server Error')
        model = TestModel
        function_name = 'create_record'

        query = '''
        query {
            users {
                id
            }
        }
        '''

        server_error = ServerError(exception, model, function_name)
        server_error.extensions['query'] = query

        self.assertEqual(server_error.code, 'ServerError')
        self.assertEqual(server_error.original_error, exception)
        self.assertEqual(server_error.message, 'User record could not be created')
        self.assertEqual(server_error.model_or_class, TestModel)
        self.assertEqual(server_error.function_name, 'create_record')
        self.assertEqual(server_error.extensions['code'], 'ServerError')
        self.assertEqual(server_error.extensions['original_error'], 'Server Error')
        self.assertEqual(server_error.extensions['model_or_class'], 'TestModel')
        self.assertEqual(server_error.extensions['function_name'], 'create_record')
        self.assertEqual(server_error.extensions['query'], query)
        self.assertTrue(isinstance(server_error.graphql_error, GraphQLError))

    def test_custom_model_error_raise_error_not_found(self):
        exception = UserModel.DoesNotExist('Not Found')
        model = UserModel
        query = '''
        query {
            users {
                id
            }
        }
        '''

        function_name = 'update_record'
        custom_model_error = CustomModelError(exception, model, function_name)

        self.assertEqual(custom_model_error.original_error, exception)
        self.assertEqual(custom_model_error.model, UserModel)

        try:
            custom_model_error.raise_error()
        except Exception as error:
            not_found_error = error

        not_found_error.extensions['query'] = query

        self.assertEqual(not_found_error.message, 'User record does not exist')
        self.assertEqual(not_found_error.extensions['code'], 'NOT_FOUND')
        self.assertEqual(not_found_error.extensions['original_error'], 'Not Found')
        self.assertEqual(not_found_error.extensions['model_or_class'], 'UserModel')
        self.assertEqual(not_found_error.extensions['function_name'], 'update_record')
        self.assertEqual(not_found_error.extensions['query'], query)

    def test_custom_model_error_raise_error_server_error(self):
        exception = Exception('Server Error')
        model = UserModel
        query = '''
        query {
            users {
                id
            }
        }
        '''

        function_name = 'create_record'
        custom_model_error = CustomModelError(exception, model,function_name)

        self.assertEqual(custom_model_error.original_error, exception)
        self.assertEqual(custom_model_error.model, UserModel)

        try:
            custom_model_error.raise_error()
        except Exception as error:
            server_error = error

        server_error.extensions['query'] = query

        self.assertEqual(server_error.message, 'User record could not be created')
        self.assertEqual(server_error.extensions['code'], 'ServerError')
        self.assertEqual(server_error.extensions['original_error'], 'Server Error')
        self.assertEqual(server_error.extensions['model_or_class'], 'UserModel')
        self.assertEqual(server_error.extensions['function_name'], 'create_record')
        self.assertEqual(server_error.extensions['query'], query)

    def test_custom_validation_error_raise_error(self):
        exception = Exception('Validation Error')
        model = TestModel
        query = '''
        query {
            users {
                id
            }
        }
        '''

        function_name = 'create_record'
        custom_model_error = CustomValidationError(exception, model, function_name)

        self.assertEqual(custom_model_error.original_error, exception)
        self.assertEqual(custom_model_error.model, TestModel)

        try:
            custom_model_error.raise_error()
        except Exception as error:
            validation_error = error

        validation_error.extensions['query'] = query

        self.assertEqual(validation_error.message, 'User input is not valid')
        self.assertEqual(validation_error.extensions['code'], 'ValidationError')
        self.assertEqual(validation_error.extensions['original_error'], 'Validation Error')
        self.assertEqual(validation_error.extensions['model_or_class'], 'TestModel')
        self.assertEqual(validation_error.extensions['function_name'], 'create_record')
        self.assertEqual(validation_error.extensions['query'], query)
