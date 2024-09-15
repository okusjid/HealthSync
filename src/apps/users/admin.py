from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Patient

# Custom User Admin Configuration
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient', 'is_staff', 'is_active')
    list_filter = ('is_doctor', 'is_patient', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        ('User Details', {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Roles', {'fields': ('is_doctor', 'is_patient')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_doctor', 'is_patient', 'is_active', 'is_staff'),
        }),
    )

# Register Doctor Model in Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Doctor Details', {'fields': ('user', 'specialization')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

# Register Patient Model in Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Patient Details', {'fields': ('user', 'date_of_birth', 'gender')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
