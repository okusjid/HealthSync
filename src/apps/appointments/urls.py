from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, AppointmentDeleteView, AppointmentUpdateView

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-detail'),
    path('<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
]
