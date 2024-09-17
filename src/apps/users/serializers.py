from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    
    This serializer handles the validation and creation of a new user, including 
    password validation and ensuring that both password fields match.
    
    Attributes:
        password: The primary password field (write-only).
        password2: A confirmation password field (write-only).
    
    Methods:
        validate: Ensures the two passwords match.
        create: Creates a new user with the provided validated data.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'is_doctor', 'is_patient']

    def validate(self, attrs):
        """
        Validates the data to ensure the password and password2 fields match.
        
        Raises:
            serializers.ValidationError: If the password fields do not match.
        
        Returns:
            attrs: The validated data.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Creates and returns a new user based on the validated data.
        
        This method uses `set_password` to hash the password before saving the user.
        
        Args:
            validated_data: The data that passed validation.
        
        Returns:
            user: The newly created user instance.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_doctor=validated_data['is_doctor'],
            is_patient=validated_data['is_patient']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Serializer for retrieving/updating user profile
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating a user's profile.
    
    This serializer is used to return or update the user's profile details, including 
    their username, email, personal information, and whether they are a doctor or patient.
    
    Attributes:
        id: The unique identifier for the user.
        username: The username of the user.
        email: The email of the user.
        first_name: The user's first name.
        last_name: The user's last name.
        phone_number: The user's phone number.
        is_doctor: Whether the user is registered as a doctor.
        is_patient: Whether the user is registered as a patient.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_doctor', 'is_patient']
