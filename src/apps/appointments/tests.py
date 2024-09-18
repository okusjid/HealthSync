from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from apps.users.models import User, Doctor, Patient


class AppointmentTests(APITestCase):
    """
    Test suite for Appointment model API interactions.
    """

    def setUp(self):
        """
        Set up initial test data, including creating users (admin, doctor, patient),
        their profiles (Doctor, Patient), and sample appointments.
        """
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpassword', email='admin@test.com'
        )

        self.doctor_user = User.objects.create_user(
            username='doctor', password='doctorpassword', email='doctor@test.com', is_doctor=True
        )

        self.patient_user = User.objects.create_user(
            username='patient', password='patientpassword', email='patient@test.com', is_patient=True
        )

        self.doctor = Doctor.objects.create(user=self.doctor_user, specialization='Cardiology')

        self.patient = Patient.objects.create(
            user=self.patient_user,
            date_of_birth='1990-01-01',
            gender='M'
        )

        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now(),
            is_completed=False
        )

        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now() - timedelta(days=2),
            is_completed=True
        )

        self.client = APIClient()

    def test_admin_can_list_appointments(self):
        """
        Ensure admin users can list all appointments.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_doctor_can_list_their_appointments(self):
        """
        Ensure doctor users can list their own appointments.
        """
        self.client.login(username='doctor', password='doctorpassword')
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_patient_cannot_list_appointments(self):
        """
        Ensure patients cannot list appointments (403 Forbidden).
        """
        self.client.login(username='patient', password='patientpassword')
        response = self.client.get(reverse('appointment-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_appointment(self):
        """
        Ensure admin users can create a new appointment.
        """
        self.client.login(username='admin', password='adminpassword')
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "scheduled_at": (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            "is_completed": False
        }
        response = self.client.post(reverse('appointment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_doctor_cannot_create_appointment(self):
        """
        Ensure doctor users cannot create appointments (403 Forbidden).
        """
        self.client.login(username='doctor', password='doctorpassword')
        data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "scheduled_at": (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            "is_completed": False
        }
        response = self.client.post(reverse('appointment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_appointment(self):
        """
        Ensure admin users can update an appointment's status.
        """
        self.client.login(username='admin', password='adminpassword')
        data = {
            "is_completed": True
        }
        response = self.client.patch(reverse('appointment-detail', args=[self.appointment1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment1.refresh_from_db()
        self.assertTrue(self.appointment1.is_completed)

    def test_doctor_cannot_update_appointment(self):
        """
        Ensure doctor users cannot update an appointment (403 Forbidden).
        """
        self.client.login(username='doctor', password='doctorpassword')
        data = {
            "is_completed": True
        }
        response = self.client.patch(reverse('appointment-detail', args=[self.appointment1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_appointment(self):
        """
        Ensure admin users can delete an appointment.
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.delete(reverse('appointment-detail', args=[self.appointment1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_doctor_cannot_delete_appointment(self):
        """
        Ensure doctor users cannot delete an appointment (403 Forbidden).
        """
        self.client.login(username='doctor', password='doctorpassword')
        response = self.client.delete(reverse('appointment-detail', args=[self.appointment1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_appointment_count_view(self):
        """
        Test the appointment count view with date range filters.
        """
        self.client.login(username='admin', password='adminpassword')
        start_date = (timezone.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        end_date = timezone.now().strftime('%Y-%m-%d')
        response = self.client.get(reverse('appointment-count'), {
            'start_date': start_date, 'end_date': end_date, 'status': 'completed'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
