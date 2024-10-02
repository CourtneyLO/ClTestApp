"""Add Module Description"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


class BaseAbstractAdmin(ImportExportModelAdmin): # pylint: disable=too-many-ancestors
    """Add Class Description"""

    readonly_fields=('id', 'created_at', 'created_by', 'updated_at', 'updated_by')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

admin.site.site_header = 'DeploymenTestAppCL'
