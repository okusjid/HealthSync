from django.db import models
from ..base_model import TimeStampedModel  # Import the base model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model extended from Django's AbstractUser.
    
    This model includes additional fields to differentiate between doctors 
    and patients, and an optional phone number field.
    
    Attributes:
        is_doctor: A boolean flag indicating whether the user is a doctor.
        is_patient: A boolean flag indicating whether the user is a patient.
        phone_number: An optional field to store the user's phone number.
    """
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        """
        String representation of the User model.
        
        Returns:
            str: The username of the user.
        """
        return self.username


class Doctor(TimeStampedModel):
    """
    Doctor model associated with a User.
    
    This model is for users who are marked as doctors and stores 
    their specialization details. It is linked to the User model 
    via a OneToOne relationship.
    
    Attributes:
        user: A OneToOne relationship with the User model, limited to users who are doctors.
        specialization: A field to store the doctor's area of specialization.
    
    Methods:
        details: Returns a formatted string with the doctor's full name and specialization.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    specialization = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation of the Doctor model.
        
        Returns:
            str: The full name and specialization of the doctor.
        """
        return f"{self.user.username} - {self.specialization} "
    def details(self):
        """
        Provides a formatted string containing the doctor's name and specialization.
        
        Returns:
            str: A string describing the doctor and their specialization.
        """
        return f"Doctor {self.user.get_full_name()} specializes in {self.specialization}."


class Patient(TimeStampedModel):
    """
    Patient model associated with a User.
    
    This model is for users who are marked as patients and stores 
    their gender and date of birth. It is linked to the User model 
    via a OneToOne relationship.
    
    Attributes:
        GENDER_CHOICES: A tuple of choices representing male and female genders.
        user: A OneToOne relationship with the User model, limited to users who are patients.
        date_of_birth: The patient's date of birth.
        gender: The patient's gender, chosen from GENDER_CHOICES.
    
    Methods:
        details: Returns a formatted string with the patient's full name, gender, and birth date.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_patient': True})
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        """
        String representation of the Patient model.
        
        Returns:
            str: The full name of the patient.
        """
        return f"Patient: {self.user.username}"

    def details(self):
        """
        Provides a formatted string containing the patient's name, gender, and date of birth.
        
        Returns:
            str: A string describing the patient, their gender, and their birth date.
        """
        return f"{self.user.username} ({self.get_gender_display()}), born on {self.date_of_birth.strftime('%b %d, %Y')}"
