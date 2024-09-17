from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

# User Registration View
class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    
    This view allows anyone (i.e., permission_classes = AllowAny) to create 
    a new user by sending a POST request with valid registration details.
    
    Attributes:
        queryset: Defines the set of user objects to interact with.
        permission_classes: Specifies that anyone can access this endpoint.
        serializer_class: Serializer class to validate and save the user data.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# User Profile View (for authenticated users)
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete the authenticated user's profile.
    
    This view allows authenticated users to access their own profile details.
    Users can retrieve their profile with a GET request, update it with a PUT
    or PATCH request, and delete their profile with a DELETE request.
    
    Attributes:
        queryset: Defines the set of user objects to interact with.
        serializer_class: Serializer class to validate and serialize the user data.
        permission_classes: Restricts access to authenticated users only.
    
    Methods:
        get_object: Overrides the method to return the authenticated user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the currently authenticated user.
        
        This method overrides the default behavior to ensure that the user 
        accessing the view can only retrieve or modify their own profile.
        
        Returns:
            The authenticated User instance.
        """
        return self.request.user  # Return the authenticated user's profile
