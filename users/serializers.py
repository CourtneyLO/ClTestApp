"""Add Module Description"""

from rest_framework import serializers

from users.errors import CustomValidationError
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    """Add Class Description"""

    class Meta:
        model = UserModel
        fields = '__all__'


class CreateSerializedUser:
    """Add Class Description"""

    def __init__(self, data, more_than_one_record=False, function_name='create_record'):
        self.data = UserSerializer(data=data, many=more_than_one_record)
        self.function_name = function_name

    def is_valid(self):
        """Add Function Description"""

        if self.data.is_valid():
            return self.data.save()

        raise CustomValidationError(self.data.errors, UserModel, self.function_name).raise_error()


class CreateSerializedUsers:
    """Add Class Description"""

    def __init__(self, data):
        self.data = data

    def is_valid(self):
        """Add Function Description"""

        return CreateSerializedUser(self.data, True, 'create_records').is_valid()


class UpdateSerializedUser:
    """Add Class Description"""

    def __init__(self, data, function_name='update_record'):
        self.function_name = function_name
        self.existing_instance = UserModel.by_id(data['id'])
        self.data = UserSerializer(self.existing_instance, data=data, partial=True)

    def is_valid(self):
        """Add Function Description"""

        if self.data.is_valid():
            return self.data.save()

        raise CustomValidationError(self.data.errors, UserModel, self.function_name).raise_error()


class UpdateSerializedUsers:
    """Add Class Description"""

    def __init__(self, data):
        self.data = data

    def is_valid(self):
        """Add Function Description"""

        records = []
        for individual_data in self.data:
            record = UpdateSerializedUser(individual_data, 'update_records').is_valid()
            records.append(record)

        return records
