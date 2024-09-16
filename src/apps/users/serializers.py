from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password



# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'is_doctor', 'is_patient']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
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
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_doctor', 'is_patient']

