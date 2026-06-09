from rest_framework import serializers

from .models import Quotation
from inquiry.serializers import InquirySerializer

class QuotationSerializer(serializers.ModelSerializer):

    inquiry_details = InquirySerializer(
        source='inquiry',
        read_only=True
    )

    class Meta:
        model = Quotation

        fields = [
            'id',
            'quotation_number',
            'amount',
            'description',
            'valid_until',
            'status',
            'inquiry',
            'inquiry_details',
            'created_at',
            'line_items'
        ]

        read_only_fields = ['quotation_number', 'created_at', 'amount']
