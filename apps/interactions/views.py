from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action in ['create', 'toggle']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        project_id = request.data.get('project')
        if not project_id:
            return Response({"detail": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR')

        if user:
            existing_like = Like.objects.filter(project_id=project_id, user=user).first()
        else:
            existing_like = Like.objects.filter(project_id=project_id, ip_address=ip_address, user__isnull=True).first()

        if existing_like:
            existing_like.delete()
            return Response({"detail": "Like removed.", "liked": False}, status=status.HTTP_200_OK)
        else:
            # Create new like
            serializer = self.get_serializer(data={'project': project_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Like added.", "liked": True}, status=status.HTTP_201_CREATED)
