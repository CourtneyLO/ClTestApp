import json
import random
import uuid
from freezegun import freeze_time
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from graphene_django.utils.testing import GraphQLTestCase

from users.schema import schema
from users.models import UserModel
from users.tests.factory import UserFactory

@freeze_time('2012-01-14')
@override_settings(DEFAULT_FILE_STORAGE='users.tests.storage.MockStorage')
class UserTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        random_number = random.randint(0, 100)
        self.user = UserFactory(name=f'A{random_number}', username=f'A{random_number}')
        self.user_2 = UserFactory(name=f'F{random_number}', username=f'F{random_number}')

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

    def test_get_users(self):
        response = self.query('''
        query {
            users {
                id
                recordId
                name
                username
                profilePicture
                createdAt
                updatedAt
            }
        }
        ''')

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['users']), 2)

        [user_1, user_2] = content['data']['users']
        self.assertEqual(user_1['recordId'], str(self.user.id))
        self.assertEqual(user_1['name'], self.user.name)
        self.assertEqual(user_1['username'], self.user.username)
        self.assertEqual(user_1['profilePicture'], self.user.profile_picture)
        self.assertEqual(user_1['createdAt'], '2012-01-14T00:00:00+00:00')
        self.assertEqual(user_1['updatedAt'], '2012-01-14T00:00:00+00:00')

        self.assertEqual(user_2['recordId'], str(self.user_2.id))
        self.assertEqual(user_2['name'], self.user_2.name)
        self.assertEqual(user_2['username'], self.user_2.username)
        self.assertEqual(user_2['profilePicture'], self.user_2.profile_picture)
        self.assertEqual(user_2['createdAt'], '2012-01-14T00:00:00+00:00')
        self.assertEqual(user_2['updatedAt'], '2012-01-14T00:00:00+00:00')

    def test_get_user_by_record_id(self):
        response = self.query('''
        query userByRecordId($recordId: UUID!) {
            userByRecordId(recordId: $recordId) {
                id
                recordId
                name
                username
                profilePicture
            }
        }
        ''',
        variables={'recordId': f'{self.user.id}'}
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)

        user = content['data']['userByRecordId']
        self.assertEqual(user['name'], self.user.name)
        self.assertEqual(user['username'], self.user.username)
        self.assertEqual(user['profilePicture'], self.user.profile_picture)

    def test_get_user_by_name(self):
        response = self.query('''
        query userByName($name: String!) {
            userByName(name: $name) {
                id
                recordId
                name
                username
                profilePicture
            }
        }
        ''',
        variables={'name': self.user.name }
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)

        user = content['data']['userByName']
        self.assertEqual(user['recordId'], str(self.user.id))
        self.assertEqual(user['name'], self.user.name)
        self.assertEqual(user['username'], self.user.username)
        self.assertEqual(user['profilePicture'], self.user.profile_picture)

    def test_get_user_by_username(self):
            response = self.query('''
            query userByUsername($username: String!) {
                userByUsername(username: $username) {
                    id
                    recordId
                    name
                    username
                    profilePicture
                }
            }
            ''',
            variables={'username': self.user.username }
            )

            content = json.loads(response.content)

            self.assertTrue('errors' not in content)

            user = content['data']['userByUsername']
            self.assertEqual(user['recordId'], str(self.user.id))
            self.assertEqual(user['name'], self.user.name)
            self.assertEqual(user['username'], self.user.username)
            self.assertEqual(user['profilePicture'], self.user.profile_picture)

    def test_get_user_by_record_id_returns_none(self):
        response = self.query('''
        query userByRecordId($recordId: UUID!) {
            userByRecordId(recordId: $recordId) {
                id
                recordId
                name
                username
                profilePicture
            }
        }
        ''',
        variables={'recordId': 'aae851e1-0d23-41eb-94d3-ece0d11a6b63'}
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)

        user = content['data']['userByRecordId']
        self.assertIsNone(user)

    def test_get_user_by_name_resturns_none(self):
        response = self.query('''
        query userByName($name: String!) {
            userByName(name: $name) {
                id
                recordId
                name
                username
                profilePicture
            }
        }
        ''',
        variables={'name': 'non_existant_name' }
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)

        user = content['data']['userByName']
        self.assertIsNone(user)

    def test_get_user_by_username_resturns_none(self):
        response = self.query('''
        query userByUsername($username: String!) {
            userByUsername(username: $username) {
                id
                recordId
                name
                username
                profilePicture
            }
        }
        ''',
        variables={'username': 'non_existant_username' }
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)

        user = content['data']['userByUsername']
        self.assertIsNone(user)

    def test_get_filtered_users_by_name_with_start_with(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Adam', username=f'Adam{random_number}')
        response = self.query('''
        query {
            filteredUsers(name_Istartswith: "a") {
            edges {
                node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
        	}
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 2)

        [user_1, user_2] = content['data']['filteredUsers']['edges']
        self.assertEqual(user_1['node']['recordId'], str(self.user.id))
        self.assertEqual(user_1['node']['name'], self.user.name)
        self.assertEqual(user_1['node']['username'], self.user.username)
        self.assertEqual(user_1['node']['profilePicture'], self.user.profile_picture)

        self.assertEqual(user_2['node']['recordId'], str(user_record.id))
        self.assertEqual(user_2['node']['name'], user_record.name)
        self.assertEqual(user_2['node']['username'], user_record.username)
        self.assertEqual(user_2['node']['profilePicture'], user_record.profile_picture)

    def test_get_filtered_users_by_name_with_contains(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Marybeth', username=f'Beth{random_number}')
        response = self.query('''
        query {
            filteredUsers(name_Icontains: "beth") {
                edges {
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
            }
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 1)

        user = content['data']['filteredUsers']['edges'][0]['node']
        self.assertEqual(user['recordId'], str(user_record.id))
        self.assertEqual(user['name'], user_record.name)
        self.assertEqual(user['username'], user_record.username)
        self.assertEqual(user['profilePicture'], user_record.profile_picture)

    def test_get_filtered_users_by_name_with_exact(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Marybeth', username=f'Beth{random_number}')
        response = self.query('''
        query {
            filteredUsers(name_Icontains: "Marybeth") {
                edges {
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
            }
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 1)

        user = content['data']['filteredUsers']['edges'][0]['node']
        self.assertEqual(user['recordId'], str(user_record.id))
        self.assertEqual(user['name'], user_record.name)
        self.assertEqual(user['username'], user_record.username)
        self.assertEqual(user['profilePicture'], user_record.profile_picture)

    def test_get_filtered_users_by_username_with_start_with(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Marybeth', username=f'Mary{random_number}')
        response = self.query('''
        query {
            filteredUsers(username_Istartswith: "m") {
                edges {
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
        	}
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 1)

        user = content['data']['filteredUsers']['edges'][0]['node']
        self.assertEqual(user['recordId'], str(user_record.id))
        self.assertEqual(user['name'], user_record.name)
        self.assertEqual(user['username'], user_record.username)
        self.assertEqual(user['profilePicture'], user_record.profile_picture)

    def test_get_filtered_users_by_username_with_contains(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Marybeth', username=f'Beth{random_number}')
        response = self.query('''
        query {
            filteredUsers(username_Icontains: "beth") {
                edges {
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
            }
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 1)

        user = content['data']['filteredUsers']['edges'][0]['node']
        self.assertEqual(user['recordId'], str(user_record.id))
        self.assertEqual(user['name'], user_record.name)
        self.assertEqual(user['username'], user_record.username)
        self.assertEqual(user['profilePicture'], user_record.profile_picture)

    def test_get_filtered_users_by_username_with_exact(self):
        random_number = random.randint(0, 100)
        user_record = UserFactory(name='Marybeth', username=f'Marybeth')
        response = self.query('''
        query {
            filteredUsers(username_Icontains: "Marybeth") {
                edges {
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
            }
        }
        '''
        )

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['filteredUsers']['edges']), 1)

        user = content['data']['filteredUsers']['edges'][0]['node']
        self.assertEqual(user['recordId'], str(user_record.id))
        self.assertEqual(user['name'], user_record.name)
        self.assertEqual(user['username'], user_record.username)
        self.assertEqual(user['profilePicture'], user_record.profile_picture)

    def test_get_user_pagination_1(self):
        response = self.query('''
        query {
            userPagination (first: 1) {
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
            }
        }
        ''')

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['userPagination']['edges']), 1)

        user_1 = content['data']['userPagination']['edges'][0]['node']
        self.assertEqual(user_1['recordId'], str(self.user.id))
        self.assertEqual(user_1['name'], self.user.name)
        self.assertEqual(user_1['username'], self.user.username)
        self.assertEqual(user_1['profilePicture'], self.user.profile_picture)

    def test_get_user_pagination_2(self):
        response = self.query('''
        query {
            userPagination (first: 2) {
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges {
                    cursor
                    node {
                        id
                        recordId
                        name
                        username
                        profilePicture
                    }
                }
        	}
        }
        ''')

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['userPagination']['edges']), 2)

        [user_1, user_2] = content['data']['userPagination']['edges']
        self.assertEqual(user_1['node']['recordId'], str(self.user.id))
        self.assertEqual(user_1['node']['name'], self.user.name)
        self.assertEqual(user_1['node']['username'], self.user.username)
        self.assertEqual(user_1['node']['profilePicture'], self.user.profile_picture)

        self.assertEqual(user_2['node']['recordId'], str(self.user_2.id))
        self.assertEqual(user_2['node']['name'], self.user_2.name)
        self.assertEqual(user_2['node']['username'], self.user_2.username)
        self.assertEqual(user_2['node']['profilePicture'], self.user_2.profile_picture)

    def test_create_user(self):
        mutation = '''
        mutation createUser($name: String!, $username: String!, $profilePicture: Upload) {
            createUser(userData: {name: $name, username: $username, profilePicture: $profilePicture}) {
                user {
                    id
                    recordId
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables = {
            'name': 'Name',
            'username': 'Username',
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

        self.assertTrue('errors' not in content)
        user = content['data']['createUser']['user']
        self.assertTrue(uuid.UUID(str(user['recordId'])))
        self.assertEqual(user['name'], variables['name'])
        self.assertEqual(user['username'], variables['username'])
        self.assertEqual(user['profilePicture'], f'{user['recordId']}/profile')

    def test_create_multiple_users(self):
        mutation ='''
        mutation createUsers($userData: [CreateUserInput!]!) {
            createUsers(userData: $userData) {
                users {
                    id
                    recordId
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables_1 = {
            'name': 'Name',
            'username': 'Username',
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

        self.assertTrue('errors' not in content)
        [user_1, user_2] = content['data']['createUsers']['users']

        self.assertTrue(uuid.UUID(str(user_1['recordId'])))
        self.assertEqual(user_1['name'], variables_1['name'])
        self.assertEqual(user_1['username'], variables_1['username'])
        self.assertEqual(user_1['profilePicture'], f'{user_1['recordId']}/profile')

        self.assertTrue(uuid.UUID(str(user_2['recordId'])))
        self.assertEqual(user_2['name'], variables_2['name'])
        self.assertEqual(user_2['username'], variables_2['username'])
        self.assertEqual(user_2['profilePicture'], f'{user_2['recordId']}/profile')

    def test_update_user_with_only_one_field_update(self):
        mutation = '''
        mutation updateUser($id: ID!, $name: String, $username: String, $profilePicture: Upload) {
            updateUser(userData: {id: $id, name: $name, username: $username, profilePicture: $profilePicture}) {
                user {
                    id
                    recordId
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables = {
            'id': f'{self.user.id}',
            'name': 'Name',
        }

        response = self.execute_multipart(mutation, variables)

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(content['data']['updateUser']['user']['recordId'], str(self.user.id))
        self.assertEqual(content['data']['updateUser']['user']['name'], variables['name'])
        self.assertEqual(content['data']['updateUser']['user']['username'], self.user.username)
        self.assertEqual(content['data']['updateUser']['user']['profilePicture'], self.user.profile_picture)

    def test_update_user(self):
        mutation = '''
        mutation updateUser($id: ID!, $name: String, $username: String, $profilePicture: Upload) {
            updateUser(userData: {id: $id, name: $name, username: $username, profilePicture: $profilePicture}) {
                user {
                    id
                    recordId
                    name
                    username
                    profilePicture
                }
            }
        }
        '''
        variables = {
            'id': f'{self.user.id}',
            'name': 'Name',
            'username': 'Username',
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

        self.assertTrue('errors' not in content)
        self.assertEqual(content['data']['updateUser']['user']['recordId'], str(self.user.id))
        self.assertEqual(content['data']['updateUser']['user']['name'], variables['name'])
        self.assertEqual(content['data']['updateUser']['user']['username'], variables['username'])
        self.assertEqual(content['data']['updateUser']['user']['profilePicture'], f'{self.user.id}/profile')

    def test_update_mulitple_users(self):
        mutation = '''
        mutation updateUsers($userData: [UserUpdateInput!]!) {
            updateUsers(userData: $userData) {
                users {
                    id
                    recordId
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
            'username': 'Username',
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

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['updateUsers']['users']), 2)

        [user_1, user_2] = content['data']['updateUsers']['users']
        self.assertEqual(user_1['recordId'], f'{self.user.id}')
        self.assertEqual(user_1['name'], variables_1['name'])
        self.assertEqual(user_1['username'], variables_1['username'])
        self.assertEqual(user_1['profilePicture'], f'{user_1['recordId']}/profile')

        self.assertEqual(user_2['recordId'], f'{self.user_2.id}')
        self.assertEqual(user_2['name'], variables_2['name'])
        self.assertEqual(user_2['username'], variables_2['username'])
        self.assertEqual(user_2['profilePicture'], f'{user_2['recordId']}/profile')

    def test_delete_user(self):
        mutation = '''
        mutation deleteUser($recordId: ID!) {
            deleteUser(recordId: $recordId) {
                result {
                    recordId
                    success
                }
            }
        }
        '''
        variables = { 'recordId': f'{self.user.id}' }
        response = self.query(mutation, variables=variables)

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(content['data']['deleteUser']['result']['recordId'], str(self.user.id))
        self.assertTrue(content['data']['deleteUser']['result']['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user.id)

    def test_delete_users(self):
        mutation = '''
        mutation deleteUsers($recordIds: [ID!]!) {
            deleteUsers(recordIds: $recordIds) {
                result {
                    recordId
                    success
                }
            }
        }
        '''
        variables = { 'recordIds': [str(self.user.id), str(self.user_2.id)] }
        response = self.query(mutation, variables=variables)

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['deleteUsers']['result']), 2)
        [deleted_user_1, deleted_user_2] = content['data']['deleteUsers']['result']

        self.assertEqual(deleted_user_1['recordId'], str(self.user.id))
        self.assertTrue(deleted_user_1['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user.id)

        self.assertEqual(deleted_user_2['recordId'], str(self.user_2.id))
        self.assertTrue(deleted_user_2['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user_2.id)

    def test_delete_user_hand(self):
        mutation = '''
        mutation deleteUser($recordId: ID!) {
            deleteUser(recordId: $recordId) {
                result {
                    recordId
                    success
                }
            }
        }
        '''
        variables = { 'recordId': f'{self.user.id}' }
        response = self.query(mutation, variables=variables)

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(content['data']['deleteUser']['result']['recordId'], str(self.user.id))
        self.assertTrue(content['data']['deleteUser']['result']['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user.id)

    def test_delete_users(self):
        mock_s3_delete = None

        mutation = '''
        mutation deleteUsers($recordIds: [ID!]!) {
            deleteUsers(recordIds: $recordIds) {
                result {
                    recordId
                    success
                }
            }
        }
        '''
        variables = { 'recordIds': [str(self.user.id), str(self.user_2.id)] }
        response = self.query(mutation, variables=variables)

        content = json.loads(response.content)

        self.assertTrue('errors' not in content)
        self.assertEqual(len(content['data']['deleteUsers']['result']), 2)
        [deleted_user_1, deleted_user_2] = content['data']['deleteUsers']['result']

        self.assertEqual(deleted_user_1['recordId'], str(self.user.id))
        self.assertTrue(deleted_user_1['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user.id)

        self.assertEqual(deleted_user_2['recordId'], str(self.user_2.id))
        self.assertTrue(deleted_user_2['success'])
        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(id=self.user_2.id)
