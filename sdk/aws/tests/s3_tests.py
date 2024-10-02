from django.test import TestCase
from unittest.mock import patch, MagicMock, Mock
import os

from sdk.aws.s3 import S3


class S3TestCase(TestCase):
    @patch('sdk.aws.s3.boto3.resource')
    def test_s3_delete(self, mock_boto3_resource):
        mock_s3_resource = MagicMock()
        mock_boto3_resource.return_value = mock_s3_resource

        mock_s3_object = Mock()
        mock_boto3_resource.Object.return_value = mock_s3_object

        s3 = S3()

        file_name = 'aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile'
        result = s3.delete(file_name)

        self.assertTrue(result)
        s3.resource.Object.assert_called_once_with(os.getenv('AWS_S3_BUCKET_NAME'), file_name)

    @patch('sdk.aws.s3.boto3.client')
    def test_get_presigned_url(self, mock_boto3_client):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_boto3_client

        mock_s3_generate_presigned_url = MagicMock()
        mock_boto3_client.generate_presigned_url.return_value = mock_s3_generate_presigned_url

        s3 = S3()
        file_name = 'aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile'
        result = s3.get_presigned_url('aae851e1-0d23-41eb-94d3-ece0d11a6b63/profile')

        self.assertTrue(result)
        s3.client.generate_presigned_url.assert_called_once_with(
            'get_object',
            Params={
                'Bucket': os.getenv('AWS_S3_BUCKET_NAME'),
                'Key': file_name ,
            },
            ExpiresIn=3600
        )
