from django.db import models
from apps.users.models import Doctor, Patient
from ..base_model import TimeStampedModel  # Import the base model

class Appointment(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} for {self.patient.user.get_full_name()} on {self.scheduled_at}"

    def details(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"Appointment with Dr. {self.doctor.user.last_name} for {self.patient.user.get_full_name()} on {self.scheduled_at.strftime('%b %d, %Y %H:%M')}. Status: {status}."
