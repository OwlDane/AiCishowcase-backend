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
            'title', 'description', 'video_url', 'github_url', 'demo_url',
            'thumbnail', 'status', 'likes_count', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'student']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'category', 'title', 'description', 
            'video_url', 'thumbnail'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        student = request.user.student_profile
        return Project.objects.create(student=student, **validated_data)
