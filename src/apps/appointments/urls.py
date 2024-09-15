from django.urls import path
from .views import AppointmentListView, AppointmentCreateView

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
]
