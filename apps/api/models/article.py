from django.db import models
from django.contrib.auth.models import User
from apps.api.models.keyword import Keyword

class Article(models.Model):
    class ArticleType(models.IntegerChoices):
        DRAFT = 0, 'Draft'
        PUBLISHED = 1, 'Published'
        ARCHIVED = 2, 'Archived'

    class ArticleStatus(models.IntegerChoices):
        PRIVATE = 0, 'Private'
        PUBLIC = 1, 'Public'

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    type = models.IntegerField(choices=ArticleType.choices, default=ArticleType.DRAFT)
    status = models.IntegerField(choices=ArticleStatus.choices, default=ArticleStatus.PRIVATE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    keywords = models.ManyToManyField(Keyword, related_name='articles')

    def __str__(self):
        return self.title