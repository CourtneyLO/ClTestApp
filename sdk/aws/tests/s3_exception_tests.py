import os
from django.test import TestCase
from unittest.mock import patch, MagicMock, Mock
from graphql import GraphQLError

from sdk.aws.s3 import S3


class S3ExceptionTestCase(TestCase):
    @patch('sdk.aws.s3.boto3.resource')
    def test_s3_delete_handles_exception(self, mock_boto3_resource):
        mock_s3_resource = MagicMock()
        mock_boto3_resource.return_value = mock_s3_resource

        mock_s3_object = Exception('Error Occured')
        mock_boto3_resource.Object.return_value = mock_s3_object

        s3 = S3()
        s3.resource.Object = Mock(side_effect=Exception('Failed to delete file from S3'))
        file_name = 'aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile'

        try:
            s3.delete(file_name)
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, f'S3 file could not be deleted from the bucket {os.getenv('AWS_S3_BUCKET_NAME')}')
        self.assertEqual(error_response.extensions['code'], 'ServerError')
        self.assertEqual(error_response.extensions['original_error'], 'Failed to delete file from S3')
        self.assertEqual(error_response.extensions['model_or_class'], 'S3')
        self.assertEqual(error_response.extensions['function_name'], 's3_delete')

    @patch('sdk.aws.s3.boto3.client')
    def test_get_presigned_url_handles_exception(self, mock_boto3_client):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_boto3_client

        s3 = S3()
        file_name = 'aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile'
        s3.client.generate_presigned_url = Mock(side_effect=Exception('Failed to generate URL'))

        try:
            s3.get_presigned_url('aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile')
        except Exception as error:
            error_response = error

        self.assertTrue(isinstance(error_response, GraphQLError))
        self.assertEqual(error_response.message, 'S3 could not create a presigned URL')
        self.assertEqual(error_response.extensions['code'], 'ServerError')
        self.assertEqual(error_response.extensions['original_error'], 'Failed to generate URL')
        self.assertEqual(error_response.extensions['model_or_class'], 'S3')
        self.assertEqual(error_response.extensions['function_name'], 's3_get_presigned_url')
