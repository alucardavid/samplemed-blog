from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="SampleMed API",
        default_version='v1',
        description="API RESTful to manage articles and comments",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API info for Swagger
api_info = openapi.Info(
    title="SampleMed API",
    default_version='v1',
    description="API RESTful to manage articles and comments",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('', include('apps.frontend.urls')),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
