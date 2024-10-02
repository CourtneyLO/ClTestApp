"""Add Module Description"""

from errors.custom import CustomError

error_messages_500 = {
    'get_record_by_id': 'Record with id, could not be retreived',
    'delete_record': 'Record could not be deleted',
    'delete_records': 'Records could not be deleted',
}


class BaseNotFoundError(CustomError):
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        code = 'NOT_FOUND'
        message = 'User record does not exist'
        super().__init__(error, model, function_name, code, message)



class BaseServerError(CustomError):
    """Add Class Description"""

    def __init__(self, model, error, function_name):
        code = 'ServerError'
        message = error_messages_500[function_name]
        super().__init__(model, error, function_name, code, message)



class BaseModelError:
    """Add Class Description"""

    def __init__(self, error, model, function_name):
        self.original_error = error
        self.model = model
        self.function_name = function_name

    def raise_error(self):
        """Add Function Description"""

        if isinstance(self.original_error, self.model.DoesNotExist):
            raise BaseNotFoundError(self.original_error, self.model, self.function_name).graphql_error

        raise BaseServerError(self.original_error, self.model, self.function_name).graphql_error
