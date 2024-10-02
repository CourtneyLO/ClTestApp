from django.test import TestCase
from graphql import GraphQLError
from freezegun import freeze_time

from errors.custom import CustomError

class TestModel:
	pass


class ErrorTestCase(TestCase):
    @freeze_time("2012-01-14")
    def test_custom_error(self):
        exception = Exception('Error')
        model = TestModel
        function_name = 'create_record'
        code = 'ERROR'
        message = 'Error occured'
        custom_error = CustomError(exception, model, function_name, code, message)

        query = '''
        query {
            users {
                id
            }
        }
        '''
        custom_error.extensions['query'] = query

        self.assertEqual(custom_error.code, 'ERROR')
        self.assertEqual(custom_error.original_error, exception)
        self.assertEqual(custom_error.message, 'Error occured')
        self.assertEqual(custom_error.model_or_class, TestModel)
        self.assertEqual(custom_error.function_name, 'create_record')
        self.assertEqual(custom_error.extensions['code'], 'ERROR')
        self.assertEqual(custom_error.extensions['original_error'], 'Error')
        self.assertEqual(custom_error.extensions['model_or_class'], 'TestModel')
        self.assertEqual(custom_error.extensions['function_name'], 'create_record')
        self.assertEqual(custom_error.extensions['query'], query)
        self.assertEqual(custom_error.extensions['timestamp'], '2012-01-14 00:00:00')
        self.assertTrue(isinstance(custom_error.graphql_error, GraphQLError))
