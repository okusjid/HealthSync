from rest_framework import generics, permissions
from .models import Appointment
from .serializers import AppointmentSerializer

# List Appointments for an authenticated user
class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the logged-in doctor
        return Appointment.objects.filter(doctor__user=self.request.user)

# Create a new Appointment
class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

# Detail View for an Appointment
class AppointmentDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the logged-in doctor
        return Appointment.objects.filter(doctor__user=self.request.user)
    
# Update an existing Appointment
class AppointmentUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter appointments for the logged-in doctor
        return Appointment.objects.filter(doctor__user=self.request.user)
    