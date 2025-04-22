from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.api.views.article import ArticleViewSet
from apps.api.views.keyword import KeywordViewSet
from apps.api.views.user import UserViewSet

# Create a router for v1 API
v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='user')
v1_router.register(r'articles', ArticleViewSet, basename='article')
v1_router.register(r'keywords', KeywordViewSet, basename='keyword')

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