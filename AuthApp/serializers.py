from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')

    def create(self, validated_data):
        # Create a new user and set the password
        user = User(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True  # You can modify this as needed (e.g., for email verification)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "email", "is_active", "created_at"]
        read_only_fields = fields

