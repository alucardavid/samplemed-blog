from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router for v1 API
v1_router = DefaultRouter()

# API v1 URL patterns
v1_urlpatterns = [
    path('', include(v1_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Main API URL patterns
urlpatterns = [
    path('v1/', include((v1_urlpatterns, 'v1'), namespace='v1')),
] 