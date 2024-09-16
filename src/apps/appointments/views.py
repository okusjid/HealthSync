# views.py
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdminUserOrReadOnlyForDoctors, IsAdminUserOrAppointmentDoctor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime



# List and create appointments (only admin can create)
class AppointmentListView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrReadOnlyForDoctors]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin users can see all appointments
            print("Admin user")
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
class AppointmentCountView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Get query parameters for date range, status, and doctor name
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status = request.query_params.get('status')  # expecting 'completed' or 'pending'
        doctor_name = request.query_params.get('doctor')  # filter by doctor's name

        # Validate the date inputs
        if not start_date or not end_date:
            return Response(
                {"error": "Please provide 'start_date' and 'end_date' query parameters in 'YYYY-MM-DD' format."},
                status=400
            )

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response(
                {"error": "Date format should be 'YYYY-MM-DD'."},
                status=400
            )

        if start_date_obj > end_date_obj:
            return Response(
                {"error": "'start_date' must be before 'end_date'."},
                status=400
            )

        # Initial filter based on date range
        appointments = Appointment.objects.filter(
            scheduled_at__date__gte=start_date_obj.date(),
            scheduled_at__date__lte=end_date_obj.date()
        )

        # Filter by status if provided
        if status:
            if status.lower() == 'completed':
                appointments = appointments.filter(is_completed=True)
            elif status.lower() == 'pending':
                appointments = appointments.filter(is_completed=False)
            else:
                return Response(
                    {"error": "Invalid status value. Use 'completed' or 'pending'."},
                    status=400
                )

        # Filter by doctor's name if provided
        if doctor_name:
            appointments = appointments.filter(
                Q(doctor__user__first_name__icontains=doctor_name) |
                Q(doctor__user__last_name__icontains=doctor_name)
            )

        # Aggregate the counts per day
        appointment_counts = appointments.annotate(
            date=TruncDate('scheduled_at')
        ).values('date').annotate(count=Count('id')).order_by('date')

        # Prepare the response data
        data = [
            {'date': entry['date'], 'appointment_count': entry['count']}
            for entry in appointment_counts
        ]

        return Response(data)
