from rest_framework import serializers
from .models import Category, Project
from apps.users.serializers import StudentProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'student', 'student_name', 'category', 'category_name', 
            'title', 'description', 'video_url', 'demo_url',
            'thumbnail', 'status', 'likes_count', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'student']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'category', 'title', 'description', 
            'video_url', 'demo_url', 'thumbnail', 
            'student', 'student_name'
        ]
        extra_kwargs = {
            'student': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        student = validated_data.pop('student', None)
        student_name = validated_data.pop('student_name', None)
        
        # If no explicit student profile provided
        if not student:
            # If user is SISWA, use their profile
            if hasattr(request.user, 'student_profile'):
                student = request.user.student_profile
            # If student_name is provided, we'll store it directly
            # but if neither, raise error
            elif not student_name:
                raise serializers.ValidationError({"student": "Either student profile or student name must be provided."})
        
        return Project.objects.create(
            student=student, 
            student_name=student_name,
            **validated_data
        )
