from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.users.models import Doctor, Patient
from .models import Appointment
from datetime import timedelta, date


class AppointmentTestCase(TestCase):
    def setUp(self):
        """
        Create initial data, including users, patients, doctors, and appointments for testing.
        """
        # Get the custom user model
        User = get_user_model()

        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

        # Create a doctor user
        self.doctor_user = User.objects.create_user(username='doctor', password='doctorpass', is_doctor=True)

        # Create a non-admin user
        self.non_admin_user = User.objects.create_user(username='nonadmin', password='nonadminpass')

        # Create a patient user
        self.patient_user = User.objects.create_user(username='patient', password='patientpass', is_patient=True)

        # Create doctor and patient profiles
        self.doctor = Doctor.objects.create(user=self.doctor_user, specialization='Cardiology')
        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth=date(1990, 1, 1),
            gender='M'
        )

        # Set up client
        self.client = APIClient()

        # Create sample appointments
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now(),
            is_completed=False
        )
        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now() + timedelta(days=1),
            is_completed=True
        )

    def test_admin_can_list_all_appointments(self):
        """
        Test that an admin can view all appointments.
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('appointment-list')  # URL for AppointmentListView
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Admin should see both appointments

    def test_admin_can_update_appointment(self):
        """
        Test that an admin can update an appointment.
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('appointment-detail', kwargs={'id': self.appointment1.id})  # URL for AppointmentDetailView
        data = {'is_completed': True}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.appointment1.refresh_from_db()
        self.assertTrue(self.appointment1.is_completed)

    def test_appointment_count_invalid_date_format(self):
        """
        Test that invalid date formats result in an error.
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('appointment-count')
        response = self.client.get(url, {'start_date': 'invalid', 'end_date': 'invalid'})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

    def test_appointment_count_view_with_valid_date_range(self):
        """
        Test that an admin can view the count of appointments filtered by a date range.
        """
        self.client.login(username='admin', password='adminpass')
        url = reverse('appointment-count')
        response = self.client.get(url, {'start_date': '2024-09-01', 'end_date': '2024-09-30'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Two appointments within the date range

    def test_appointment_detail_doctor_can_retrieve_own_appointment(self):
        """
        Test that a doctor can retrieve the details of their own appointment.
        """
        self.client.login(username='doctor', password='doctorpass')
        url = reverse('appointment-detail', kwargs={'id': self.appointment1.id})  # URL for AppointmentDetailView
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.appointment1.id)

    def test_doctor_can_only_view_their_own_appointments(self):
        """
        Test that a doctor can only view their own appointments.
        """
        self.client.login(username='doctor', password='doctorpass')
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # The doctor should see both appointments

    def test_doctor_cannot_update_appointment(self):
        """
        Test that a doctor cannot update an appointment (only view).
        """
        self.client.login(username='doctor', password='doctorpass')
        url = reverse('appointment-detail', kwargs={'id': self.appointment1.id})
        data = {'is_completed': True}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, 403)  # Doctors cannot update appointments

    def test_non_admin_cannot_create_appointment(self):
        """
        Test that a non-admin user cannot create an appointment.
        """
        self.client.login(username='nonadmin', password='nonadminpass')
        url = reverse('appointment-list')
        data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'scheduled_at': timezone.now(),
            'is_completed': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 403)  # Non-admin users cannot create appointments
