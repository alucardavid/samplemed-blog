from rest_framework import serializers
from apps.api.models.keyword import Keyword

class BaseKeywordSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        return value.strip().lower()
    
class KeywordSerializer(BaseKeywordSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'name')

class KeywordCreateSerializer(BaseKeywordSerializer):
    class Meta:
        model = Keyword
        fields = ('name',)
        extra_kwargs = {
            'name': {'validators': []}  # Remove validação de unicidade automática
        }
    