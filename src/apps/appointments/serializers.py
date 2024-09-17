# serializers.py
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Appointment model.
    
    This serializer is used for creating, retrieving, updating, and validating
    appointment data. It ensures that only admin users (staff members) can 
    create or modify appointments.
    
    Attributes:
        Meta: Defines the model and fields to be serialized.
    
    Methods:
        validate: Validates the request to ensure only admin users can create 
                  or modify appointments.
    """
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'scheduled_at', 'is_completed']

    def validate(self, data):
        """
        Validates that only admin users can create or modify appointments.
        
        Args:
            data: The incoming data for validation.
        
        Raises:
            serializers.ValidationError: If the user is not a staff member.
        
        Returns:
            data: The validated data.
        """
        request = self.context.get('request')
        if not request.user.is_staff:
            raise serializers.ValidationError("Only admin users can create or modify appointments.")
        return data
