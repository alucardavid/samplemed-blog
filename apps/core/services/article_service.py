from apps.api.models.article import Article
from typing import Dict, List
from django.contrib.auth.models import User
from apps.api.serializers.keyword import KeywordCreateSerializer
from apps.core.services.keyword_service import KeywordService

class ArticleService:
    """
    Service class for managing articles.
    """
    @staticmethod
    def get_articles_by_author(author: User) -> List[Article]:
        """
        Retrieves all articles by a specific author.
        
        Args:
            author (User): The author whose articles to retrieve.
        
        Returns:
            List[Article]: A list of articles by the specified author.
        """
        return Article.objects.filter(author=author).select_related('author')

    @staticmethod
    def create_article(article_data: Dict, author: User) -> Article:
        """
        Creates a new article.
        
        Args:
            article_ddata (Dict): The data for the article to be created.
            author (User): The author of the article.
        
        Returns:
            article_db (Article): The created article instance.
        
        """
        # Extract keywords from article data
        keywords = article_data.pop('keywords', [])

        # Add author to article data
        article_data['author'] = author

        # Create article
        article = Article.objects.create(**article_data)

        # Set keywords for the article
        keywords_objs = []
        if keywords:
            for name in keywords:
                serializer = KeywordCreateSerializer(data={'name': name})
                serializer.is_valid(raise_exception=True)
                keyword = serializer.save()
                keywords_objs.append(keyword)
        article.keywords.set(keywords_objs)
        return article
    
    
        

    