from rest_framework import serializers

from .models import Payment
from projects.serializers import ProjectSerializer

class PaymentSerializer(serializers.ModelSerializer):
    project_details = ProjectSerializer(
        source='project',
        read_only=True
    )

    class Meta:
        model = Payment

        fields = [
            'id',
            'project',
            'project_details',
            'amount',
            'payment_method',
            'transaction_id',
            'created_at'
        ]
