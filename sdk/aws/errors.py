"""Add Module Description"""

import os

from errors.custom import CustomError

error_messages_500 = {
	's3_delete': f'S3 file could not be deleted from the bucket {os.getenv("AWS_S3_BUCKET_NAME")}',
	's3_get_presigned_url': 'S3 could not create a presigned URL',
}


class ServerError(CustomError):
    """Add Class Description"""

    def __init__(self, model, error, function_name):
        code = 'ServerError'
        message = error_messages_500[function_name]
        super().__init__(model, error, function_name, code, message)


class CustomClassError:
    """Add Class Description"""

    def __init__(self, error, custom_class, function_name):
        self.original_error = error
        self.custom_class = custom_class
        self.function_name = function_name

    def raise_error(self):
        """Add Function Description"""

        raise ServerError(self.original_error, self.custom_class, self.function_name).graphql_error
