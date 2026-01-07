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
            'id', 'student', 'category', 'category_name', 
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
            'video_url', 'demo_url', 'thumbnail', 'student'
        ]
        extra_kwargs = {
            'student': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        student = validated_data.pop('student', None)
        
        # If no student provided, try to use the logged in user's profile (SISWA logic)
        if not student and hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            
        if not student:
            raise serializers.ValidationError({"student": "A student must be assigned to the project."})
            
        return Project.objects.create(student=student, **validated_data)
