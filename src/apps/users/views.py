from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# User Profile View (for authenticated user)
class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the authenticated user's profile
