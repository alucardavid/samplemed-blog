from rest_framework import viewsets, permissions, status, pagination
from rest_framework.response import Response
from apps.api.models.keyword import Keyword
from apps.api.serializers.keyword import KeywordCreateSerializer, KeywordSerializer
from apps.core.services.keyword_service import KeywordService
from apps.core.exceptions.business_exceptions import BusinessException
from django_filters.rest_framework import DjangoFilterBackend

class KeywordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing keyword operations.
    
    This viewset provides the following actions:
    - Create keyword (POST /keywords/)
    
    Authentication:
    - Reading/creating/updating/deleting requires authentication
    """
    
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return KeywordCreateSerializer
        return KeywordSerializer

    def create(self, request):
        """
        Create a new keyword instance.

        Args:
            request: The HTTP request containing the keyword data.

        Returns:
            Keyword: The created keyword instance.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            keyword = KeywordService.create_keyword(serializer.validated_data['name'])
            response_serializer = KeywordSerializer(keyword)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except BusinessException as e:
            return Response({"error": str(e.default_detail)}, status=e.status_code)