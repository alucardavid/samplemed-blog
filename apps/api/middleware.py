from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JSONMiddleware(MiddlewareMixin):
    """
    Middleware that ensures all 404, 500 responses are JSON.
    This middleware runs before Django's default 404 and 500 handlers.
    """
    def process_response(self, request, response):
        # Handle 404 errors for API paths
        if response.status_code == 404 and request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Not found',
                'detail': 'The requested resource was not found on this server.',
                'status_code': 404,
                'path': request.path
            }, status=404)

        # Handle 500 errors for API paths
        if response.status_code == 500 and request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Internal Server Error',
                'detail': 'An unexpected error occurred.',
                'status_code': 500,
                'path': request.path
            }, status=500)

        return response

    def process_exception(self, request, exception):
        # Handle exceptions for API paths
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Internal Server Error',
                'detail': str(exception),
                'status_code': 500,
                'path': request.path
            }, status=500)