from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'full_name', 'angkatan', 'bio', 'photo', 'github_url', 'linkedin_url']

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'student_profile', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', User.Role.PUBLIC)
        )
        return user
