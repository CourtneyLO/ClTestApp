"""Add Module Description"""

# TODO: Add error logging

import datetime
import pytz
from graphql import GraphQLError

class CustomError:
    """Add Class Description"""

    def __init__(self, error, model_or_class, function_name, code, message):
        # TODO: ensure we add userId # pylint: disable=fixme
        self.code = code
        self.original_error = error
        self.message = message
        self.model_or_class = model_or_class
        self.timestamp = datetime.datetime.now(pytz.timezone('Europe/London'))
        self.function_name = function_name
        self.extensions = {
            'code': self.code,
            'original_error': str(self.original_error),
            'model_or_class': self.model_or_class.__name__,
            'function_name': self.function_name,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'query': ''
        }
        self.graphql_error = GraphQLError(self.message, extensions=self.extensions)
