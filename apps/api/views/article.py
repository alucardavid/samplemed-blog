from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apps.api.models.article import Article
from apps.core.services.article_service import ArticleService
from apps.core.exceptions.business_exceptions import BusinessException
from apps.api.serializers.article import ArticleSerializer, ArticleCreateSerializer
from django.contrib.auth.models import User

class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing article operations.
    
    This viewset provides the following actions:
    - List articles (GET /articles/)
    - Create article (POST /articles/)
    - Retrieve article (GET /articles/{id}/)
    - Update article (PUT/PATCH /articles/{id}/)
    - Delete article (DELETE /articles/{id}/)
    - Get articles by author (GET /articles/author/{author_id}/)
    
    Authentication:
    - Reading/creating/updating/deleting requires authentication
    """
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        return ArticleSerializer
    
    def create(self, request):
        """
        Create a new article.

        Parameters:
            - request (Request): The request object containing the article data.

        Returns:
            - Response: A JSON response containing the created article data.
        
        Exceptions:
            - ValidationError: If the provided data is invalid.
            - BusinessException: If there is a business logic error during article creation.
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            article = ArticleService.create_article(serializer.validated_data, user)
            return Response(ArticleSerializer(article).data, status=status.HTTP_201_CREATED)
        except BusinessException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='author/(?P<author_id>[^/.]+)')
    def by_author(self, request, author_id=None):
        """
        Retrieve all articles by a specific author.

        Parameters:
            - author_id (int): The ID of the author whose articles to retrieve

        Returns:
            - Response: A JSON response containing the author's articles

        Exceptions:
            - BusinessException: If there is an error retrieving the articles
            - NotFound: If the author does not exist
        """
        try:
            # Get the author
            author = User.objects.get(id=author_id)
            
            # Get articles by author
            articles = ArticleService.get_articles_by_author(author)
            
            # Serialize and return the articles
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            raise NotFound(f"Author with id {author_id} not found")
        except BusinessException as e:
            return Response({"error": str(e.default_detail)}, status=e.status_code)