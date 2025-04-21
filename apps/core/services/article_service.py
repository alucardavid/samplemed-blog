from datetime import datetime, timezone
from django.db.models import Q
from apps.api.models.article import Article
from typing import Dict, List, Optional
from django.contrib.auth.models import User
from apps.core.exceptions.business_exceptions import ArticleNotFoundError, UnauthorizedError
from apps.api.serializers.article import ArticleCreateSerializer

class ArticleService:
    """
    Service class for managing articles.
    """

    @staticmethod
    def get_all_articles() -> List[Article]:
        """
        Retrieves all articles from the database.
        
        Returns:
            List[Article]: A list of all articles.
        """
        return Article.objects.select_related('author').all()
    
    @staticmethod
    def get_article_by_id(article_id: int) -> Optional[Article]:
        """
        Retrieves an article by its ID.
        
        Args:
            article_id (int): The ID of the article to retrieve.
        
        Returns:
            Optional[Article]: The article if found, otherwise None.
        
        Raises:
            ArticleNotFoundError: If the article with the given ID does not exist.
        """
        try:
            return Article.objects.select_related('author').get(id=article_id)
        except Article.DoesNotExist:
            raise ArticleNotFoundError(f"Article with id {article_id} not found.")
    
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
        # Add author to article data
        article_data['author'] = author

        # Create article
        article_db = Article.objects.create(**article_data)
        article_db.save()
        article_db.refresh_from_db()

        return article_db
    
    @staticmethod
    def update_article(article: Article, article_data: Dict, author: User) -> Article:
        """
        Updates an existing article.
        
        Args:
            article_id (int): The ID of the article to update.
            article_data (Dict): The data for the article to be updated.
            author (User): The author of the article.
        
        Returns:
            Article: The updated article instance.
        
        Raises:
            ArticleNotFoundError: If the article with the given ID does not exist.
        """
        # Check if the author is the same as the one who created the article
        if article.author != author:
            raise UnauthorizedError("You are not authorized to update this article.")

        # Update the article
        for key, value in article_data.items():
            setattr(article, key, value)

        article.updated_at = datetime.now(timezone.utc)

        # Save and refresh the article
        article.save()
        article.refresh_from_db()

        return article
    
    @staticmethod
    def delete_article(article: Article, author: User) -> None:
        """
        Deletes an article.
        
        Args:
            article (Article): The article to delete.
            author (User): The author of the article.
        
        Raises:
            UnauthorizedError: If the author is not authorized to delete the article.
        """
        # Check if the author is the same as the one who created the article
        if article.author != author:
            raise UnauthorizedError("You are not authorized to delete this article.")

        # Delete the article
        article.delete()
        

    