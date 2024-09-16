from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .models import Doctor, Patient
from .serializers import RegisterSerializer, UserSerializer, DoctorSerializer, PatientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# User Profile View (for authenticated users)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the authenticated user's profile
