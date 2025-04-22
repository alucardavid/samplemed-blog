from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessException(APIException):
    """
    Base class for all business exceptions in the application.
    
    This exception should be used for all business rule violations
    and domain-specific errors that need to be communicated to the client.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business rule violation occurred'
    default_code = 'business_error'

class ArticleNotFoundError(BusinessException):
    """
    Exception raised when an article cannot be found.
    
    This exception is raised when:
    - An article with the specified ID doesn't exist
    - The article has been deleted
    - The article is not accessible to the current user
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Article not found'
    default_code = 'article_not_found'

class UnauthorizedError(BusinessException):
    """
    Exception raised when a user doesn't have permission to perform an action.
    
    This exception is raised when:
    - A user tries to access a private article they don't own
    - A user tries to modify content they don't own
    - A user tries to perform an action without proper authentication
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action'
    default_code = 'unauthorized'

class ValidationError(BusinessException):
    """
    Exception raised when data validation fails.
    
    This exception is raised when:
    - Required fields are missing
    - Field values are invalid
    - Business rules for data validation are violated
    """
    default_detail = 'Validation error'
    default_code = 'validation_error'

class CommentNotFoundError(BusinessException):
    """
    Exception raised when a comment cannot be found.
    
    This exception is raised when:
    - A comment with the specified ID doesn't exist
    - The comment has been deleted
    - The comment is not accessible to the current user
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Comment not found'
    default_code = 'comment_not_found'

class KeywordNotFoundError(BusinessException):
    """
    Exception raised when a keyword cannot be found.
    
    This exception is raised when:
    - A keyword with the specified ID doesn't exist
    - The keyword has been deleted
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Keyword not found'
    default_code = 'keyword_not_found'

class UserNotFoundError(BusinessException):
    """
    Exception raised when a user cannot be found.
    
    This exception is raised when:
    - A user with the specified ID doesn't exist
    - The user has been deleted
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found'
    default_code = 'user_not_found'

class DuplicateKeywordError(BusinessException):
    """
    Exception raised when attempting to create a duplicate keyword.
    
    This exception is raised when:
    - A keyword with the same name already exists
    - Case-insensitive matching finds a duplicate
    """
    default_detail = 'Keyword already exists'
    default_code = 'duplicate_keyword'

class InvalidArticleStatusError(BusinessException):
    """
    Exception raised when an invalid article status is provided.
    
    This exception is raised when:
    - An invalid status value is provided
    - The status transition is not allowed
    """
    default_detail = 'Invalid article status'
    default_code = 'invalid_article_status'

class InvalidArticleTypeError(BusinessException):
    """
    Exception raised when an invalid article type is provided.
    
    This exception is raised when:
    - An invalid type value is provided
    - The type is not supported
    """
    default_detail = 'Invalid article type'
    default_code = 'invalid_article_type' 