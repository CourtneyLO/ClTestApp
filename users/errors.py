"""Add Module Description"""

from errors.custom import CustomError

error_messages_500 = {
    'create_record': 'User record could not be created',
    'create_records': 'User records could not be created',
    'update_record': 'User record could not be updated',
    'update_records': 'User records could not be updated',
    'delete_record': 'User record could not be deleted',
    'delete_records': 'User records could not be deleted',
    'get_record_by_id': 'User record could not be retreived by id given',
    'get_record_by_name': 'User record could not be retreived by name given',
}


class NotFoundError(CustomError):
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        code = 'NOT_FOUND'
        message = 'User record does not exist'
        super().__init__(error, model, function_name, code, message)


class ValidationError(CustomError):
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        code = 'ValidationError'
        message = 'User input is not valid'
        super().__init__(error, model, function_name, code, message)


class ServerError(CustomError):
    """Add Class Description"""

    def __init__(self, model, error, function_name):
        code = 'ServerError'
        message = error_messages_500[function_name]
        super().__init__(model, error, function_name, code, message)



class CustomModelError:
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        self.original_error = error
        self.model = model
        self.function_name = function_name

    def raise_error(self):
        """Add Function Description"""

        if isinstance(self.original_error, self.model.DoesNotExist):
            raise NotFoundError(self.original_error, self.model, self.function_name).graphql_error

        raise ServerError(self.original_error, self.model, self.function_name).graphql_error


class CustomValidationError:
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        self.original_error = error
        self.model = model
        self.function_name = function_name

    def raise_error(self):
        """Add Function Description"""

        raise ValidationError(self.original_error, self.model, self.function_name).graphql_error
