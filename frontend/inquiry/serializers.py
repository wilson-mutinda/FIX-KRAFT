from rest_framework import serializers
from .models import Inquiry
from clients.models import Client


class InquirySerializer(serializers.ModelSerializer):

    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    phone = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    company = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    client_details = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry

        fields = [
            'id',
            'name',
            'email',
            'phone',
            'company',
            'service',
            'budget',
            'message',
            'quotation_amount',
            'due_date',
            'status',
            'client',
            'client_details',
            'created_at'
        ]

        read_only_fields = [
            'client',
            'client_details',
            'created_at'
        ]

    def get_client_details(self, obj):

        return {
            'id': obj.client.id,
            'name': obj.client.name,
            'email': obj.client.email,
            'phone': obj.client.phone,
            'company': obj.client.company
        }

    def create(self, validated_data):

        name = validated_data.pop('name')
        email = validated_data.pop('email')

        phone = validated_data.pop(
            'phone',
            ''
        )

        company = validated_data.pop(
            'company',
            ''
        )

        client, created = Client.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
                'company': company
            }
        )

        # UPDATE EXISTING CLIENT DETAILS
        if not created:

            client.name = name

            if phone:
                client.phone = phone

            if company:
                client.company = company

            client.save()

        inquiry = Inquiry.objects.create(
            client=client,
            **validated_data
        )

        return inquiry