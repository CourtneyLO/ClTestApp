import json
# import requests
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene_django.utils.testing import GraphQLTestCase

from users.schema import schema
from users.models import UserModel
from users.tests.factory import UserFactory


@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class UserExceptionTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = UserFactory(name='A')
        self.user_2 = UserFactory(name='F')

    def execute_multipart(self, query, variables=None, files=None):
        operations = {
            'query': query,
            'variables': variables or {}
        }

        if files == None:
            body = { 'operations': json.dumps(operations) }
            return self.client.post('/graphql', data=body, format='multipart')
        elif len(files) >= 2:
            files_map = {str(i): [f"variables.userData.{key}.profilePicture"] for i, key in enumerate(files.keys())}
        else:
            files_map = {str(i): [f"variables.profilePicture"] for i, key in enumerate(files.keys())}

        body = {
            'operations': json.dumps(operations),
            'map': json.dumps(files_map),
        }
        body.update({str(i): file for i, file in enumerate(files.values())})

        return self.client.post('/graphql', data=body, format='multipart')

    def test_create_user_handles_exceptions(self):
        mutation = '''
        mutation createUser($name: String!, $username: String!, $profilePicture: Upload) {
            createUser(userData: {name: $name, username: $username, profilePicture: $profilePicture}) {
            user {
                    id
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables = {
            'name': self.user.name,
            'username': self.user.username,
            'profilePicture': None
        }
        fake_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'these are the contents of the fake image file',
            content_type='image/jpeg'
        )
        files = {
            'profilePicture': fake_image
        }

        response = self.execute_multipart(mutation, variables, files)

        content = json.loads(response.content)

        self.assertIsNotNone(content.get('errors'))
        errors = content.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['message'], 'User input is not valid')
        self.assertEqual(errors[0]['path'], ['createUser'])
        self.assertEqual(len(errors[0]['extensions']), 6)
        self.assertEqual(errors[0]['extensions']['code'], 'ValidationError')
        self.assertEqual(errors[0]['extensions']['original_error'], "{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}")
        self.assertEqual(errors[0]['extensions']['model_or_class'], 'UserModel')
        self.assertEqual(errors[0]['extensions']['function_name'], 'create_record')
        self.assertEqual(errors[0]['extensions']['query'], mutation)

    def test_create_multiple_users_handles_exceptions(self):
        mutation ='''
        mutation createUsers($userData: [CreateUserInput!]!) {
            createUsers(userData: $userData) {
                users {
                    id
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables_1 = {
            'name': self.user.name,
            'username': self.user.username,
            'profilePicture': None
        }
        variables_2 = {
            'name': 'Name2',
            'username': 'Username2',
            'profilePicture': None
        }
        fake_image_1 = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'these are the contents of the fake image file',
            content_type='image/jpeg'
        )
        fake_image_2 = SimpleUploadedFile(
            name='test_image_1.jpg',
            content=b'these are the contents of the fake image file 2',
            content_type='image/jpeg'
        )
        files = { '0': fake_image_1, '1': fake_image_2 }

        variables = { 'userData': [variables_1, variables_2]}
        response = self.execute_multipart(mutation, variables, files)

        content = json.loads(response.content)

        self.assertIsNotNone(content.get('errors'))
        errors = content.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['message'], 'User input is not valid')
        self.assertEqual(errors[0]['path'], ['createUsers'])
        self.assertEqual(len(errors[0]['extensions']), 6)
        self.assertEqual(errors[0]['extensions']['code'], 'ValidationError')
        self.assertEqual(errors[0]['extensions']['original_error'], "[{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}, {}]")
        self.assertEqual(errors[0]['extensions']['model_or_class'], 'UserModel')
        self.assertEqual(errors[0]['extensions']['function_name'], 'create_records')
        self.assertEqual(errors[0]['extensions']['query'], mutation)

    def test_update_user_handles_exceptions(self):
        mutation = '''
        mutation updateUser($id: ID!, $name: String, $username: String, $profilePicture: Upload) {
            updateUser(userData: {id: $id, name: $name, username: $username, profilePicture: $profilePicture}) {
                user {
                    id
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables = {
            'id': f'{self.user.id}',
            'name': self.user.name,
            'username': self.user_2.username,
            'profilePicture': None
        }
        fake_image = SimpleUploadedFile(
            name='replace_test_image.jpg',
            content=b'these are the contents of the fake image file',
            content_type='image/jpeg'
        )
        files = {
            'profilePicture': fake_image
        }

        response = self.execute_multipart(mutation, variables, files)
        content = json.loads(response.content)

        self.assertIsNotNone(content.get('errors'))
        errors = content.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['message'], 'User input is not valid')
        self.assertEqual(errors[0]['path'], ['updateUser'])
        self.assertEqual(len(errors[0]['extensions']), 6)
        self.assertEqual(errors[0]['extensions']['code'], 'ValidationError')
        self.assertEqual(errors[0]['extensions']['original_error'], "{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}")
        self.assertEqual(errors[0]['extensions']['model_or_class'], 'UserModel')
        self.assertEqual(errors[0]['extensions']['function_name'], 'update_record')
        self.assertEqual(errors[0]['extensions']['query'], mutation)

    def test_update_mulitple_users_handles_exceptions(self):
        mutation = '''
        mutation updateUsers($userData: [UserUpdateInput!]!) {
            updateUsers(userData: $userData) {
                users {
                    id
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables_1 = {
            'id': f'{self.user.id}',
            'name': 'Name',
            'username': self.user_2.username,
            'profilePicture': None
        }
        variables_2 = {
            'id': f'{self.user_2.id}',
            'name': 'Name2',
            'username': 'Username2',
            'profilePicture': None
        }
        fake_image_1 = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'these are the contents of the fake image file',
            content_type='image/jpeg'
        )
        fake_image_2 = SimpleUploadedFile(
            name='test_image_1.jpg',
            content=b'these are the contents of the fake image file 2',
            content_type='image/jpeg'
        )
        files = { '0': fake_image_1, '1': fake_image_2 }

        variables = { 'userData': [variables_1, variables_2]}
        response = self.execute_multipart(mutation, variables, files)

        content = json.loads(response.content)

        self.assertIsNotNone(content.get('errors'))
        errors = content.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['message'], 'User input is not valid')
        self.assertEqual(errors[0]['path'], ['updateUsers'])
        self.assertEqual(len(errors[0]['extensions']), 6)
        self.assertEqual(errors[0]['extensions']['code'], 'ValidationError')
        self.assertEqual(errors[0]['extensions']['original_error'], "{'username': [ErrorDetail(string='User with this username already exists.', code='unique')]}")
        self.assertEqual(errors[0]['extensions']['model_or_class'], 'UserModel')
        self.assertEqual(errors[0]['extensions']['function_name'], 'update_records')
        self.assertEqual(errors[0]['extensions']['query'], mutation)
