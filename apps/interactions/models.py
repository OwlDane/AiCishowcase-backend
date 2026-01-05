import uuid
from django.db import models
from django.conf import settings
from apps.projects.models import Project

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='likes')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')  # For authenticated users
        # For non-authenticated, we will handle logic in view/serializer using ip_address

    def __str__(self):
        return f"{self.user or self.ip_address} liked {self.project.title}"
