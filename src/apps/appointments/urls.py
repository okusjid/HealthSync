# urls.py
from django.urls import path
from .views import AppointmentListView, AppointmentDetailView

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('<int:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
]
