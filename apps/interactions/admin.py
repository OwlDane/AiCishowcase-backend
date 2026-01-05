from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project__title', 'user__username', 'ip_address')
