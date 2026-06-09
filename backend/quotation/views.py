from django.shortcuts import render
from rest_framework import viewsets
from .models import Quotation
from .serializers import QuotationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from .pdf_generator import generate_quotation_pdf
from rest_framework.permissions import IsAuthenticated
from clients.models import Client

class QuotationViewSet(viewsets.ModelViewSet):
    serializer_class = QuotationSerializer

    def get_queryset(self):
        queryset = Quotation.objects.all().order_by('-created_at')
        inquiry_id = self.request.query_params.get('inquiry')
        if inquiry_id:
            queryset = queryset.filter(inquiry_id=inquiry_id)
        return queryset

    @action(detail=True, methods=['post'])
    def email_quotation(self, request, pk=None):
        quotation = self.get_object()
        client = quotation.inquiry.client

        pdf_buffer = generate_quotation_pdf(quotation)

        subject = f"Your Quotation from FixKraft Digital - {quotation.quotation_number}"
        body = f"""
        Dear {client.name},

        Thank you for your interest in FixKraft Digital.

        Please find attached your quotation ({quotation.quotation_number}) for your review.

        Quotation Details:
        - Total Amount: KSh {float(quotation.amount):,.2f}
        - Valid Until: {quotation.valid_until}

        To view or download the PDF, please open the attached file.

        If you have any questions, please don't hesitate to contact us.

        Best regards,
        FixKraft Digital Team
        info@fixkraftdigital.com | +254 748 929 891
        """

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[client.email],
        )
        email.attach(f"Quotation_{quotation.quotation_number}.pdf", pdf_buffer.getvalue(), 'application/pdf')

        try:
            email.send()
            return Response({"message": "Quotation emailed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_quotations(self, request):
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response({"detail": "Client profile not found."}, status=404)
        
        quotations = Quotation.objects.filter(inquiry__client=client)
        serializer = self.get_serializer(quotations, many=True)
        return Response(serializer.data)