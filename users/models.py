"""Add Module Description"""

from django.db import models

from main.model import BaseAbstractModel
from main.constants import NULL_AND_BLANK
from users.errors import CustomModelError

def user_directory_path(instance, _):
    """Add Function Description"""

    return f'{instance.id}/profile'


class UserModel(BaseAbstractModel):
    """Add Class Description"""

    class Meta:
        verbose_name = "User"
        ordering = ["name"]

    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.FileField(upload_to=user_directory_path, **NULL_AND_BLANK)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Add Function Description"""

        self.profile_picture.delete()
        super().delete()

    @classmethod
    def by_name(cls, name, accepts_does_not_exist=False):
        """Add Function Description"""

        try:
            return cls.objects.get(name=name)
        except Exception as error:
            if accepts_does_not_exist and isinstance(error, cls.DoesNotExist):
                return None # pylint: disable-msg=E0702

            raise CustomModelError(error, cls, 'get_record_by_name').raise_error()

    @classmethod
    def by_username(cls, username, accepts_does_not_exist=False):
        """Add Function Description"""

        try:
            return cls.objects.get(username=username)
        except Exception as error:
            if accepts_does_not_exist and isinstance(error, cls.DoesNotExist):
                return None # pylint: disable-msg=E0702

            raise CustomModelError(error, cls, 'get_record_by_username').raise_error()
