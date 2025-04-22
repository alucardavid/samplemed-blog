from rest_framework import serializers
from apps.api.models.article import Article
from apps.api.models.comment import Comment
from apps.api.serializers.user import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'article', 'created_at')
        read_only_fields = ('author',) 