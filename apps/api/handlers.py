from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

def custom_exception_handler(exc, context):
    """
    Custom exception handler for API errors.
    Returns JSON responses for all error types.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, NotFound):
            return JsonResponse({
                'error': 'Not found',
                'detail': str(exc),
                'status_code': status.HTTP_404_NOT_FOUND,
                'path': context['request'].path
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Handle other exceptions
        return JsonResponse({
            'error': 'Server error',
            'detail': str(exc),
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'path': context['request'].path
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Customize the error response
    response.data = {
        'error': response.status_text,
        'detail': response.data,
        'status_code': response.status_code,
        'path': context['request'].path
    }

    return response

def handler404(request, exception):
    """
    Custom 404 handler that returns JSON response for API requests.
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not found',
            'detail': 'The requested resource was not found on this server.',
            'status_code': 404,
            'path': request.path
        }, status=404)
    
    # For non-API requests, return the default 404 template
    from django.views.defaults import page_not_found
    return page_not_found(request, exception)

def handler500(request):
    """
    Custom 500 handler that returns JSON response for API requests.
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Server error',
            'detail': 'An internal server error occurred.',
            'status_code': 500,
            'path': request.path
        }, status=500)
    
    # For non-API requests, return the default 500 template
    from django.views.defaults import server_error
    return server_error(request) 