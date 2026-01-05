from django.contrib import admin
from .models import Category, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'student__angkatan')
    search_fields = ('title', 'description', 'student__full_name')
    actions = ['approve_projects', 'reject_projects']

    def approve_projects(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_projects.short_description = "Approve selected projects"

    def reject_projects(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_projects.short_description = "Reject selected projects"
