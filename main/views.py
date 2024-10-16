"""Add Module Description"""

import sentry_sdk
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.generic import ListView
from django.http import JsonResponse


class CustomGraphQLView(FileUploadGraphQLView):
    """Add Class Description"""

    def execute_graphql_request(self, request, data, query, *args, **kwargs):
        result = super().execute_graphql_request(request, data, query, *args, **kwargs)

        if result.errors:
            for error in result.errors:
                message = f'Error: {error.message} for {error.path}'
                if 'extensions' in error.formatted:
                    error.formatted['extensions']['query'] = query
                    with sentry_sdk.push_scope() as scope:
                        for key in error.formatted['extensions']:
                            # TODO: ensure we add userId # pylint: disable=fixme
                            scope.set_extra(key, error.formatted['extensions'][key])
                            sentry_sdk.capture_message(message)
                else:
                    sentry_sdk.capture_message(message)

        return result

class HealthCheck(ListView):
    """Add Class Description"""

    def get(self, *args, **kwargs):
        return JsonResponse({'response': 'ok'}, status=200)
