from django.contrib import admin
from .models import User, StudentProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'angkatan')
    search_fields = ('full_name', 'user__username', 'angkatan')
