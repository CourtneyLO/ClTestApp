import os
from django.test import TestCase
from graphql import GraphQLError

from sdk.aws.errors import CustomClassError

class TestClass:
    pass


class ErrorTestCase(TestCase):
    def test_sdk_error_raise_class_error(self):
        exception = Exception('Server Error')
        custom_class = TestClass
        query = '''
        query {
            users {
                id
            }
        }
        '''

        function_name = 's3_delete'
        custom_error = CustomClassError(exception, custom_class, function_name)

        self.assertEqual(custom_error.original_error, exception)
        self.assertEqual(custom_error.custom_class, TestClass)

        try:
            custom_error.raise_error()
        except Exception as error:
            class_error = error

        class_error.extensions['query'] = query

        self.assertEqual(class_error.message, f'S3 file could not be deleted from the bucket {os.getenv('AWS_S3_BUCKET_NAME')}')
        self.assertEqual(class_error.extensions['code'], 'ServerError')
        self.assertEqual(class_error.extensions['original_error'], 'Server Error')
        self.assertEqual(class_error.extensions['function_name'], 's3_delete')
        self.assertEqual(class_error.extensions['query'], query)
