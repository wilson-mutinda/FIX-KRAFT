from rest_framework import serializers
from .models import Mediahub
from Category.serializers import MediaCategorySerializer

class MediahubSerializer(serializers.ModelSerializer):

    category_details = MediaCategorySerializer(
        source='category',
        read_only=True
    )

    class Meta:
        model = Mediahub

        fields = [
            'id',
            'file',
            'title',
            'description',
            'uploaded_at',
            'updated_at',
            'category',
            'category_details',
            'is_deleted'
        ]

        read_only_fields = [
            'uploaded_at',
            'updated_at'
        ]

