from rest_framework import viewsets, permissions, pagination
from apps.api.models.comment import Comment
from apps.api.serializers.comment import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
@method_decorator(cache_page(60 * 5), name='list')
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comment operations.
    
    This viewset provides the following actions:
    - Create comment (POST /comments/)
    
    Authentication:
    - Creating/updating/deleting requires authentication
    """
    
    queryset = Comment.objects.all().select_related('author')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article', 'author', 'content']
    

    def perform_create(self, serializer):
        cache.clear()
        serializer.save(author=self.request.user)