from rest_framework import serializers
from apps.api.models.article import Article
from apps.api.serializers.user import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'content', 'type', 'status', 'author', 'created_at', 'updated_at')
        read_only_fields = ('author',)

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'subtitle', 'content', 'type', 'status')
        read_only_fields = ('author',)

class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'subtitle', 'content', 'type', 'status')
        read_only_fields = ('author',)