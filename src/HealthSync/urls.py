from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import Group
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="HealthSync API",
        default_version='v1',
        description="API documentation for HealthSync",
        contact=openapi.Contact(email="support@healthsync.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin Panel
    path('users/', include('apps.users.urls')),  # User-related URLs
    path('appointments/', include('apps.appointments.urls')),  # Appointment-related URLs
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT Token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT Token
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify JWT Token
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI (optional)
]

# Customize Admin Titles
admin.site.site_header = "HealthSync Admin"
admin.site.site_title = "HealthSync Admin Portal"
admin.site.index_title = "Welcome to HealthSync Admin Portal"

# Unregister the Group model from admin since it may not be used
admin.site.unregister(Group)
