from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.SISWA:
        StudentProfile.objects.get_or_create(user=instance, defaults={'full_name': instance.username})

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()
