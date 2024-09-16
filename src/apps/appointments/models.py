from django.db import models
from apps.users.models import Doctor, Patient
from ..base_model import TimeStampedModel

class Appointment(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        doctor_name = self.doctor.user.last_name or "Unknown Doctor"
        patient_name = self.patient.user.get_full_name() or "Unknown Patient"
        return f"Appointment with Dr. {doctor_name} for {patient_name} on {self.scheduled_at}"

    def details(self):
        status = "Completed" if self.is_completed else "Pending"
        doctor_name = self.doctor.user.last_name or "Unknown Doctor"
        patient_name = self.patient.user.get_full_name() or "Unknown Patient"
        scheduled_time = self.scheduled_at.strftime('%b %d, %Y %H:%M')
        return f"Appointment with Dr. {doctor_name} for {patient_name} on {scheduled_time}. Status: {status}."
