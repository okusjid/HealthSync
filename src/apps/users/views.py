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



# Doctor View (retrieve and update doctor details)
class DoctorView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     # Assuming Doctor model has a OneToOneField with the User model
    #     try:
    #         return self.request
    #     except Doctor.DoesNotExist:
    #         raise Http404("Doctor not found")

        
# Patient View (retrieve and update patient details)
class PatientView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.patient  # Retrieve the patient's profile based on the logged-in user

# # Logout View (Token Blacklist)
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"detail": "Logout successful."})
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)