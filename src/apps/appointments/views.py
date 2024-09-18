import logging
from rest_framework import generics, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdminUserOrReadOnlyForDoctors, IsAdminUserOrAppointmentDoctor
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination


# List and create appointments (only admin can create)
class AppointmentListView(generics.ListCreateAPIView):
    """
    View for listing and creating appointments.
    
    This view allows the listing of appointments for admin and doctors. Admins can view
    all appointments and create new ones, while doctors can only view their own appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrAppointmentDoctor]

    def get_queryset(self):
        """
        Returns the appropriate set of appointments based on the user's role.
        
        Admins see all appointments, while doctors see only their appointments.
        Non-admin, non-doctor users have no access.
        
        Returns:
            QuerySet: A filtered set of appointments.
        """
        user = self.request.user
        try:
            if user.is_staff:
                return Appointment.objects.all()
            elif hasattr(user, 'doctor'):
                return Appointment.objects.filter(doctor=user.doctor)
            else:
                return Appointment.objects.none()
        except Exception as e:
            logging.error(f"Error retrieving appointments: {e}")
            return Appointment.objects.none()

    def perform_create(self, serializer):
        """
        Handles the creation of a new appointment.
        
        Only admin users can create appointments, and this method saves the 
        appointment instance.
        """
        try:
            serializer.save()
        except Exception as e:
            logging.error(f"Error creating appointment: {e}")
            raise ValidationError("An error occurred while creating the appointment.")


# Retrieve, update, and delete appointments (only admin can update/delete)
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting an appointment.
    
    This view allows admins and doctors to view appointments. However, only admins
    are allowed to update or delete appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUserOrReadOnlyForDoctors]
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
        try:
            if user.is_staff:
                return Appointment.objects.all()
            elif hasattr(user, 'doctor'):
                return Appointment.objects.filter(doctor=user.doctor)
            else:
                return Appointment.objects.none()
        except Exception as e:
            logging.error(f"Error retrieving appointment details: {e}")
            return Appointment.objects.none()

    def perform_update(self, serializer):
        """
        Handles the update of an appointment. Only admin users can update appointments.
        """
        try:
            serializer.save()
        except Exception as e:
            logging.error(f"Error updating appointment: {e}")
            raise ValidationError("An error occurred while updating the appointment.")

    def perform_destroy(self, instance):
        """
        Handles the deletion of an appointment. Only admin users can delete appointments.
        """
        try:
            instance.delete()
        except Exception as e:
            logging.error(f"Error deleting appointment: {e}")
            raise ValidationError("An error occurred while deleting the appointment.")


class AppointmentCountView(APIView):
    """
    View to provide the count of appointments over time based on filters.
    This view allows admin users to retrieve the count of appointments over a specified
    date range, optionally filtered by status (completed/pending) and doctor's name.
    """
    permission_classes = [permissions.IsAdminUser]

    start_date_param = openapi.Parameter(
        'start_date', openapi.IN_QUERY, description="Start date for the date range (YYYY-MM-DD)", type=openapi.TYPE_STRING
    )
    end_date_param = openapi.Parameter(
        'end_date', openapi.IN_QUERY, description="End date for the date range (YYYY-MM-DD)", type=openapi.TYPE_STRING
    )
    status_param = openapi.Parameter(
        'status', openapi.IN_QUERY, description="Filter by status (completed/pending)", type=openapi.TYPE_STRING
    )
    doctor_name_param = openapi.Parameter(
        'doctor', openapi.IN_QUERY, description="Filter by doctor's name", type=openapi.TYPE_STRING
    )


    @swagger_auto_schema(manual_parameters=[start_date_param, end_date_param, status_param, doctor_name_param])
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status = request.query_params.get('status')
        doctor_name = request.query_params.get('doctor')

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

        try:
            filters = Q(scheduled_at__date__gte=start_date_obj.date(), scheduled_at__date__lte=end_date_obj.date())

            if status:
                if status.lower() == 'completed':
                    filters &= Q(is_completed=True)
                elif status.lower() == 'pending':
                    filters &= Q(is_completed=False)
                else:
                    return Response(
                        {"error": "Invalid status value. Use 'completed' or 'pending'."},
                        status=400
                    )

            if doctor_name:
                filters &= Q(doctor__user__username__icontains=doctor_name)

            appointment_counts = Appointment.objects.filter(filters) \
                .annotate(date=TruncDate('scheduled_at')) \
                .values('date') \
                .annotate(count=Count('id')) \
                .order_by('date')

            if not appointment_counts:
                return Response({"message": "No appointments found for the given criteria."}, status=404)

            data = [
                {'date': entry['date'], 'appointment_count': entry['count']}
                for entry in appointment_counts
            ]

            
            # paginator = PageNumberPagination()
            # paginator.page_size = 5  # Set page size to 5 appointments per page
            # paginated_data = paginator.paginate_queryset(data, request)

            # return paginator.get_paginated_response(paginated_data)

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=500)
