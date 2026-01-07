from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Project
from .serializers import CategorySerializer, ProjectSerializer, ProjectCreateSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'student__angkatan', 'status']
    search_fields = ['title', 'description', 'student__full_name']
    ordering_fields = ['created_at', 'likes_count']

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Project.objects.all()
        if self.action in ['list', 'retrieve']:
            # Only show approved projects to public
            if not self.request.user.is_authenticated or self.request.user.role != 'ADMIN':
                queryset = queryset.filter(status=Project.Status.APPROVED)
        
        # If user is SISWA, they can see their own projects regardless of status in special action
        return queryset

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_projects(self, request):
        if request.user.role != 'SISWA':
            return Response({"detail": "Only students have projects."}, status=status.HTTP_403_FORBIDDEN)
        
        projects = Project.objects.filter(student=request.user.student_profile)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        project = self.get_object()
        project.status = Project.Status.APPROVED
        project.save()
        return Response({'status': 'project approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        project = self.get_object()
        project.status = Project.Status.REJECTED
        project.save()
        return Response({'status': 'project rejected'})
