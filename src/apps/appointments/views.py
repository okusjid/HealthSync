# views.py
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdminUserOrReadOnlyForDoctors, IsAdminUserOrAppointmentDoctor

# List and create appointments (only admin can create)
class AppointmentListView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrReadOnlyForDoctors]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin users can see all appointments
            return Appointment.objects.all()
        elif hasattr(user, 'doctor'):
            # Doctors can see their own appointments
            return Appointment.objects.filter(doctor=user.doctor)
        else:
            # Other users have no access
            return Appointment.objects.none()

    def perform_create(self, serializer):
        # Only admin users can create appointments
        serializer.save()

# Retrieve, update, and delete appointments (only admin can update/delete)
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrAppointmentDoctor]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin users can access all appointments
            return Appointment.objects.all()
        elif hasattr(user, 'doctor'):
            # Doctors can access their own appointments
            return Appointment.objects.filter(doctor=user.doctor)
        else:
            # Other users have no access
            return Appointment.objects.none()
