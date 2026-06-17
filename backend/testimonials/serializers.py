from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'client_name', 'logo', 'website_url', 'testimonial_text', 'client_role', 'display_order', 'is_active']
