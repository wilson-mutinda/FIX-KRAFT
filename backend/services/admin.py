from django.contrib import admin

from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_order', 'is_active', 'created_at']
    list_editable = ['display_order', 'is_active']
    search_fields = ['title', 'description']
    list_filter = ['is_active']
    ordering = ['display_order']
