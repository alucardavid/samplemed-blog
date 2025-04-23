from django.db import models
from apps.api.models.article import Article
from django.contrib.auth.models import User

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'