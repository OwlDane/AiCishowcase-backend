from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'project', 'user', 'ip_address', 'created_at']
        read_only_fields = ['user', 'ip_address']

    def validate(self, data):
        project = data['project']
        request = self.context.get('request')
        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR')

        # Check for existing like
        if user:
            if Like.objects.filter(project=project, user=user).exists():
                raise serializers.ValidationError("You have already liked this project.")
        else:
            if Like.objects.filter(project=project, ip_address=ip_address, user__isnull=True).exists():
                raise serializers.ValidationError("You have already liked this project from this IP.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user if request.user.is_authenticated else None
        validated_data['ip_address'] = request.META.get('REMOTE_ADDR')
        return super().create(validated_data)
