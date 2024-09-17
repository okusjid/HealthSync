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
    """
    View for listing and creating appointments.
    
    This view allows the listing of appointments for admin and doctors. Admins can view
    all appointments and create new ones, while doctors can only view their own appointments.
    
    Attributes:
        serializer_class: Serializer to handle Appointment data.
        permission_classes: Permission checks, allowing only admins to create appointments.
    
    Methods:
        get_queryset: Returns a filtered queryset based on the user's role (admin/doctor).
        perform_create: Saves a new appointment, allowed only for admin users.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrReadOnlyForDoctors]

    def get_queryset(self):
        """
        Returns the appropriate set of appointments based on the user's role.
        
        Admins see all appointments, while doctors see only their appointments.
        Non-admin, non-doctor users have no access.
        
        Returns:
            QuerySet: A filtered set of appointments.
        """
        user = self.request.user
        if user.is_staff:
            print("Admin user")
            return Appointment.objects.all()
        elif hasattr(user, 'doctor'):
            return Appointment.objects.filter(doctor=user.doctor)
        else:
            return Appointment.objects.none()

    def perform_create(self, serializer):
        """
        Handles the creation of a new appointment.
        
        Only admin users can create appointments, and this method saves the 
        appointment instance.
        
        Args:
            serializer: The validated serializer data for the appointment.
        """
        serializer.save()


# Retrieve, update, and delete appointments (only admin can update/delete)
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting an appointment.
    
    This view allows admins and doctors to view appointments. However, only admins
    are allowed to update or delete appointments.
    
    Attributes:
        serializer_class: Serializer to handle Appointment data.
        permission_classes: Permission checks to restrict update/delete access to admins.
        lookup_field: The field used to look up the appointment by ID.
    
    Methods:
        get_queryset: Returns a filtered queryset based on the user's role (admin/doctor).
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrAppointmentDoctor]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Returns the appropriate set of appointments based on the user's role.
        
        Admins see all appointments, while doctors see only their appointments.
        Non-admin, non-doctor users have no access.
        
        Returns:
            QuerySet: A filtered set of appointments.
        """
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif hasattr(user, 'doctor'):
            return Appointment.objects.filter(doctor=user.doctor)
        else:
            return Appointment.objects.none()


# View for counting appointments over time, filtered by date range, status, and doctor
class AppointmentCountView(APIView):
    """
    View to provide the count of appointments over time based on filters.
    
    This view allows admin users to retrieve the count of appointments over a specified
    date range, optionally filtered by status (completed/pending) and doctor's name.
    
    Attributes:
        permission_classes: Permission checks to allow access only to admin users.
    
    Methods:
        get: Handles GET requests to return the count of appointments per day, with optional filters.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Handles GET requests to return the count of appointments per day, filtered by date range, status, and doctor.
        
        Args:
            request: The incoming request with query parameters for filtering (start_date, end_date, status, doctor).
        
        Returns:
            Response: A JSON response containing the count of appointments per day.
        """
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
