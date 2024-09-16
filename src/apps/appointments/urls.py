# urls.py
from django.urls import path
from .views import AppointmentListView, AppointmentDetailView, AppointmentCountView

urlpatterns = [
    path('appointments/list/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/count/', AppointmentCountView.as_view(), name='appointment-count'),
]
