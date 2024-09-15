from django.db import models
from ..base_model import TimeStampedModel  # Import the base model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Doctor(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

    def details(self):
        return f"Doctor {self.user.get_full_name()} specializes in {self.specialization}."


class Patient(TimeStampedModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_patient': True})
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

    def details(self):
        return f"{self.user.get_full_name()} ({self.get_gender_display()}), born on {self.date_of_birth.strftime('%b %d, %Y')}"
