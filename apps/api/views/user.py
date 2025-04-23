from rest_framework import viewsets, permissions, status, pagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from apps.core.services.user_service import UserService
from apps.core.exceptions.business_exceptions import BusinessException
from apps.api.serializers.user import UserSerializer, UserRegistrationSerializer

User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user operations.
    
    This viewset provides the following actions:
    - List users (GET /users/)
    - Create user (POST /users/)
    - Retrieve user (GET /users/{id}/)
    - Update user (PUT/PATCH /users/{id}/)
    - Delete user (DELETE /users/{id}/)
    
    Authentication:
    - Reading users is allowed for all users
    - Creating/updating/deleting requires authentication
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Override default permissions to allow unauthenticated access to the create method.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def create(self, request):
        """
        Creates a new user.
        
        Args:
            request: Request object containing user data
            
        Raises:
            BusinessException: If there's an error creating the user
        """
        serializer = UserRegistrationSerializer(data=request.data)
    
        if serializer.is_valid():
            try:
                tokens = UserService.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data.get('first_name', ''),
                    last_name=serializer.validated_data.get('last_name', '')
                )
                return Response(tokens, status=status.HTTP_201_CREATED)
            except BusinessException as e:
                return Response({'error': str(e)}, status=400)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        """
        Updates an existing user.
        
        Args:
            request: Request object containing the user data to update
            pk: Primary key of the user to update
            
        Raises:
            ValidationError: If there's an error updating the user
            BUsinessException: If there's an error updating the user
            PermissionDenied: If user doesn't have permission to update the user
        """
        
        # Retrieve the user instance to update
        user = User.objects.filter(id=pk).first()

        if not user:
            raise NotFound('User not found')

        # Initialize the serializer with the existing user instance
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            try:
                updated_user = UserService.update_user(user, serializer.validated_data)
                return Response(self.get_serializer(updated_user).data, status=status.HTTP_200_OK)
            except BusinessException as e:
                raise ValidationError({'error': str(e)})
            except PermissionDenied as e:
                raise
            except Exception as e:
                raise ValidationError({'error': 'Error updating user'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """
        Deletes a user.
        
        Args:
            request: Request object
            pk: Primary key of the user to delete

        Raises:
            BusinessException: If there's an error deleting the user
            NotFound: If the user does not exist
            PermissionDenied: If user doesn't have permission to delete the user
        """
        try:
            # Retrieve the user instance to delete
            user = User.objects.filter(id=pk).first()

            # Check if the user exists
            if not user:
                raise NotFound('User not found')

            UserService.delete_user(self, user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BusinessException as e:
            raise ValidationError({'error': str(e)})
        except PermissionDenied as e:
            raise
        except Exception as e:
            raise ValidationError({'error': 'Error deleting user'})

    