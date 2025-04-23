from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.api.models.article import Article
from apps.api.models.keyword import Keyword

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Criar artigo de teste
        self.article = Article.objects.create(
            title='Test Article',
            subtitle='Test Subtitle',
            content='Test Content',
            author=self.user,
            type=Article.ArticleType.PUBLISHED,
            status=Article.ArticleStatus.PUBLIC
        )
        
        # Criar keyword de teste
        self.keyword = Keyword.objects.create(name='test')
        self.article.keywords.add(self.keyword)

    def authenticate(self):
        """Helper method to authenticate requests"""
        self.client.force_authenticate(user=self.user)