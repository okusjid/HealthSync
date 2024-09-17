from django.contrib import admin
from .models import Appointment

# Register Appointment Model in Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Appointment model.
    
    This class defines how the Appointment model will be displayed and managed in the 
    Django admin interface. It customizes the list display, search functionality, filters, 
    and fieldsets for better organization and usability.
    
    Attributes:
        list_display: Fields that will be displayed in the list view in the admin interface.
        list_filter: Fields to filter the list view in the admin interface.
        search_fields: Fields to search by in the admin interface.
        readonly_fields: Fields that are read-only in the admin form (cannot be edited).
        fieldsets: Layout of the fields in the admin form, organized into sections.
    """
    
    list_display = ('patient', 'doctor', 'scheduled_at', 'is_completed', 'created_at', 'updated_at')
    """
    Defines which fields to display in the list view of appointments.
    
    Fields:
        patient: Displays the patient associated with the appointment.
        doctor: Displays the doctor associated with the appointment.
        scheduled_at: Shows the scheduled time of the appointment.
        is_completed: Indicates whether the appointment is completed or not.
        created_at: Timestamp for when the appointment was created.
        updated_at: Timestamp for when the appointment was last updated.
    """

    list_filter = ('is_completed', 'scheduled_at')
    """
    Adds filtering options in the admin interface.
    
    Fields:
        is_completed: Filter by whether the appointment is completed.
        scheduled_at: Filter by the scheduled date and time of the appointment.
    """

    search_fields = ('patient__user__username', 'doctor__user__username', 'scheduled_at')
    """
    Enables search functionality in the admin interface.
    
    Fields:
        patient__user__username: Search by the patient's username.
        doctor__user__username: Search by the doctor's username.
        scheduled_at: Search by the scheduled date of the appointment.
    """

    readonly_fields = ('created_at', 'updated_at')
    """
    Makes the following fields read-only in the admin form:
    
    Fields:
        created_at: The appointment creation timestamp (non-editable).
        updated_at: The timestamp for the last update of the appointment (non-editable).
    """

    fieldsets = (
        ('Appointment Details', {'fields': ('patient', 'doctor', 'scheduled_at', 'is_completed')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    """
    Organizes the form fields into sections in the admin interface:
    
    Sections:
        'Appointment Details': Includes patient, doctor, scheduled_at, and is_completed fields.
        'Timestamps': Includes created_at and updated_at fields.
    """
