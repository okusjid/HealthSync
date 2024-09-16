# serializers.py
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'scheduled_at', 'is_completed']

    def validate(self, data):
        # Only admin users can create or modify appointments
        request = self.context.get('request')
        if not request.user.is_staff:
            raise serializers.ValidationError("Only admin users can create or modify appointments.")
        return data
