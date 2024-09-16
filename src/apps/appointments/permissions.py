# permissions.py
from rest_framework import permissions

class IsAdminUserOrReadOnlyForDoctors(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete appointments.
    Allows doctors to read (GET) their own appointments.
    """

    def has_permission(self, request, view):
        # Admin users have full access
        if request.user and request.user.is_staff:
            return True

        # Allow doctors to perform safe methods
        if request.method in permissions.SAFE_METHODS and hasattr(request.user, 'doctor'):
            return True

        # Deny access otherwise
        return False

class IsAdminUserOrAppointmentDoctor(permissions.BasePermission):
    """
    Object-level permission to only allow admin users or the doctor assigned to the appointment to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user and request.user.is_staff:
            return True

        # Allow doctors to access their own appointments
        if hasattr(request.user, 'doctor') and obj.doctor == request.user.doctor:
            return request.method in permissions.SAFE_METHODS

        # Deny access otherwise
        return False
