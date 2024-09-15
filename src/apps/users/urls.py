from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, DoctorView, PatientView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('doctor/', DoctorView.as_view(), name='doctor'),
    path('patient/', PatientView.as_view(), name='patient'),
]
