from rest_framework import serializers
from apps.api.models.article import Article
from apps.api.serializers.keyword import KeywordSerializer
from apps.api.serializers.user import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'content', 'type', 'status', 'keywords', 'author', 'created_at', 'updated_at')
        read_only_fields = ('author',)

class ArticleCreateSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    class Meta:
        model = Article
        fields = ('title', 'subtitle', 'content', 'type', 'status', 'keywords')
        read_only_fields = ('author',)

