"""Add Module Description"""

import os
import boto3

from .errors import CustomClassError

class S3:
    """Add Class Description"""

    def __init__(self):
        self.resource = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.bucket = os.getenv('AWS_S3_BUCKET_NAME')

    def delete(self, file_name):
        """Add Function Description"""

        try:
            return self.resource.Object(self.bucket, file_name).delete()
        except Exception as error:
            raise CustomClassError(error, S3, 's3_delete').raise_error()

    def get_presigned_url(self, file_name):
        """Add Function Description"""

        try:
            return self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': f"{file_name}",
                },
                ExpiresIn=3600  # URL expiration time in seconds
            )
        except Exception as error:
            raise CustomClassError(error, S3, 's3_get_presigned_url').raise_error()
