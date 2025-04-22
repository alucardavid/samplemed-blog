from django.db.models import Q
from apps.api.models.keyword import Keyword
from apps.core.exceptions.business_exceptions import BusinessException, KeywordNotFoundError

class KeywordService:
    """
    Service class for managing keyword operations.
    
    This service provides methods for:
    - Creating keywords
    - Updating keywords
    - Deleting keywords
    - Checking permissions
    - Filtering keywords
    """
   
    @staticmethod
    def create_keyword(name: str) -> Keyword:
        """
        Create a new keyword.
        
        Args:
            name (str): The name of the keyword.
        
        Returns:
            Keyword: The created keyword object.
        
        """
        keyword, created = Keyword.objects.get_or_create(name=name)

        return keyword