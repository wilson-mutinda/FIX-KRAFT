from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'display_order', 'is_active', 'created_at']
    list_editable = ['display_order', 'is_active']
    search_fields = ['client_name', 'testimonial_text']
    list_filter = ['is_active']
    ordering = ['display_order']