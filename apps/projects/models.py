import uuid
from django.db import models
from apps.users.models import StudentProfile

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Project(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)
    demo_url = models.URLField(max_length=500, blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
