from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Dict, List, Tuple
from django.db import transaction
from apps.api.serializers.user import UserSerializer
from ..exceptions.business_exceptions import ValidationError

class UserService:
    """
    Service class for managing user-related operations.
    
    This service handles all user-related functionality including:
    - User registration with JWT token generation
    - Profile retrieval with statistics
    - Profile updates
    
    All operations are performed with proper error handling and transaction management
    where necessary.
    """

    @staticmethod
    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.
        
        Returns:
            Dict: A dictionary containing all user instances
        """
        queryset = User.objects.all()
        serialized_users = UserSerializer(queryset, many=True).data

        return serialized_users
    
    @staticmethod
    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            User: The user instance with the specified ID
            
        Raises:
            ValidationError: If the user does not exist
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist")
        
    @staticmethod
    def create_user(username: str, email: str, password: str, 
                   first_name: str = '', last_name: str = '') -> Tuple[User, Dict]:
        """
        Creates a new user and returns the user instance along with JWT tokens.
        
        Args:
            username (str): Unique username for the new user
            email (str): Email address for the new user
            password (str): Password for the new user
            first_name (str, optional): User's first name. Defaults to empty string
            last_name (str, optional): User's last name. Defaults to empty string
            
        Returns:
            Tuple[User, Dict]: A tuple containing:
                - User: The newly created user instance
                - Dict: JWT tokens (access and refresh) for the user
                
        Raises:
            ValidationError: If user creation fails for any reason
            
        Note:
            This operation is wrapped in a transaction to ensure data consistency
        """
        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                
                return tokens
                
            except Exception as e:
                raise ValidationError(f"Error creating user: {str(e)}")

    @staticmethod
    def get_user_profile(user: User) -> Dict:
        """
        Retrieves a user's profile including activity statistics.
        
        Args:
            user (User): The user whose profile to retrieve
            
        Returns:
            Dict: A dictionary containing:
                - Basic user information (id, username, email, names)
                - Activity counts (articles, comments)
                
        Note:
            This method performs efficient database queries by using
            the reverse relationships defined in the User model
        """
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'articles_count': user.articles.count(),
            'comments_count': user.comments.count()
        }
    
    @staticmethod
    def update_user(user: User, data: Dict) -> User:
        """
        Updates a user's information.
        
        Args:
            user (User): The user to update
            data (Dict): Dictionary containing the fields to update:
                - username (optional): New username
                - email (optional): New email address
                - first_name (optional): New first name
                - last_name (optional): New last name
                
        Returns:
            User: The updated user instance
            
        Note:
            Only specified fields in the data dictionary will be updated
        """
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in data:
                setattr(user, field, data[field])
                
        user.save()
        return user

    def delete_user(self, user: User) -> None:
        """
        Deletes a user from the database.
        
        Args:
            user (User): The user to delete
            
        Note:
            This operation is wrapped in a transaction to ensure data consistency
        """
        with transaction.atomic():
            user.delete()