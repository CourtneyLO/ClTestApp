"""Add Module Description"""

from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.conf import settings

from .errors import BaseModelError
from .constants import NULL_AND_BLANK

class BaseAbstractModel(models.Model):
    """Add Class Description"""

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_%(class)s_set',
        on_delete=models.CASCADE,
        **NULL_AND_BLANK
    )
    updated_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='updated_%(class)s_set',
        on_delete=models.CASCADE,
        **NULL_AND_BLANK
    )

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save()

    @classmethod
    def by_id(cls, record_id, accepts_does_not_exist=False):
        """Add Function Description"""

        try:
            return cls.objects.get(pk=record_id)
        except Exception as error:
            if accepts_does_not_exist and isinstance(error, cls.DoesNotExist):
                return None # pylint: disable-msg=E0702

            raise BaseModelError(error, cls, 'get_record_by_id').raise_error()

    @classmethod
    def delete_record(cls, record_id):
        """Add Function Description"""

        try:
            cls.objects.get(pk=record_id).delete()
        except Exception as error:
            if isinstance(error, cls.DoesNotExist):
                return None # pylint: disable-msg=E0702

            raise BaseModelError(error, cls, 'delete_record').raise_error()

        return id

    @classmethod
    def delete_records(cls, ids):
        """Add Function Description"""

        results = []
        try:
            records = cls.objects.filter(pk__in=ids)
            for record in records:
                record_id = record.id
                record.delete()
                results.append({ 'record_id': record_id, 'success': True })
        except Exception as error:
            raise BaseModelError(error, cls, 'delete_records').raise_error() # pylint: disable-msg=E0702

        return results
