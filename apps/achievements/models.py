import uuid
from django.db import models

class Achievement(models.Model):
    class Category(models.TextChoices):
        COMPETITION = 'Competition', 'Competition'
        RECOGNITION = 'Recognition', 'Recognition'
        PARTNERSHIP = 'Partnership', 'Partnership'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    date = models.CharField(max_length=100)  # e.g., "October 2023"
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.RECOGNITION)
    link = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
