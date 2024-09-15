from django.contrib import admin
from .models import Appointment

# Register Appointment Model in Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_at', 'is_completed', 'created_at', 'updated_at')
    list_filter = ('is_completed', 'scheduled_at')
    search_fields = ('patient__user__username', 'doctor__user__username', 'scheduled_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Appointment Details', {'fields': ('patient', 'doctor', 'scheduled_at', 'is_completed')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
