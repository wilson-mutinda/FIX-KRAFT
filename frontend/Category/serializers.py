from rest_framework import serializers
from .models import MediaCategory

class MediaCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaCategory

        fields = [
            'id',
            'name',
            'slug',
            'description',
            'created_at',
            'updated_at',
            'is_deleted'
        ]

        read_only_fields = [
            'slug',
            'created_at',
            'updated_at'
        ]
