from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from apps.api.models.comment import Comment
from apps.api.serializers.comment import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comment operations.
    
    This viewset provides the following actions:
    - List comments (GET /comments/)
    - Create comment (POST /comments/)
    - Retrieve comment (GET /comments/{id}/)
    - Update comment (PUT/PATCH /comments/{id}/)
    - Delete comment (DELETE /comments/{id}/)
    
    Authentication:
    - Reading comments is allowed for all users
    - Creating/updating/deleting requires authentication
    """
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)