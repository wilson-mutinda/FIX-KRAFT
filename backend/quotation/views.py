from django.shortcuts import render
from rest_framework import viewsets
from .models import Quotation
from .serializers import QuotationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils import timezone
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

        # Generate PDF
        pdf_buffer = generate_quotation_pdf(quotation)

        # --- Build HTML email content ---
        amount_formatted = f"{float(quotation.amount):,.2f}"
        valid_until = quotation.valid_until.strftime('%B %d, %Y')
        today = timezone.now().date().strftime('%B %d, %Y')

        # Build line items table
        line_items_html = ""
        for item in quotation.line_items:
            service = item.get('service', '')
            price = float(item.get('price', 0))
            line_items_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{service}</td>
                <td style="padding: 10px; border-bottom: 1px solid #e0e0e0; text-align: right;">KSh {price:,.2f}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Quotation {quotation.quotation_number}</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; padding: 20px; background: #f9f9f9; }}
                .container {{ max-width: 700px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
                .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #e5a233; padding-bottom: 15px; margin-bottom: 20px; }}
                .header h1 {{ font-size: 26px; color: #1b325e; margin: 0; }}
                .header .ref {{ font-size: 14px; color: #777; }}
                .info-row {{ display: flex; justify-content: space-between; background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }}
                .info-row strong {{ color: #1b325e; }}
                .description {{ background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th {{ background: #1b325e; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #e0e0e0; }}
                .total-row {{ background: #f0f4f8; font-weight: bold; }}
                .total-row td {{ border-bottom: none; padding: 12px; }}
                .payment-methods {{ background: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .payment-methods ul {{ list-style: none; padding: 0; display: flex; gap: 15px; flex-wrap: wrap; }}
                .payment-methods ul li {{ font-size: 14px; }}
                .terms {{ margin-top: 20px; padding-top: 15px; border-top: 1px solid #e0e0e0; font-size: 12px; color: #555; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #e0e0e0; padding-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div>
                        <h1>QUOTATION</h1>
                        <p class="ref">{quotation.quotation_number}</p>
                    </div>
                </div>

                <div class="info-row">
                    <div>
                        <strong>Client:</strong> {client.name}<br>
                        <strong>Email:</strong> {client.email}<br>
                        <strong>Phone:</strong> {client.phone or '—'}<br>
                        <strong>Company:</strong> {client.company or 'N/A'}
                    </div>
                    <div style="text-align: right;">
                        <strong>Date:</strong> {today}<br>
                        <strong>Valid Until:</strong> {valid_until}
                    </div>
                </div>

                <div class="description">
                    <strong>Description of Work</strong>
                    <p style="margin: 5px 0 0;">{quotation.description or '—'}</p>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th style="text-align: right;">Amount (KSh)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {line_items_html}
                        <tr class="total-row">
                            <td><strong>Total</strong></td>
                            <td style="text-align: right;"><strong>{amount_formatted}</strong></td>
                        </tr>
                    </tbody>
                </table>

                <div class="payment-methods">
                    <strong>Payment Options</strong>
                    <ul>
                        <li>🏦 Bank Transfer (Equity, KCB, Co-operative)</li>
                        <li>📱 M-Pesa (Paybill: 123456, Account: Invoice #)</li>
                        <li>💳 Credit/Debit Card (via PayPal/Stripe)</li>
                    </ul>
                </div>

                <div class="terms">
                    <strong>Terms & Conditions</strong>
                    <ul>
                        <li>This quotation is valid until {valid_until}.</li>
                        <li>Payment is due within <strong>7 working days</strong> of acceptance.</li>
                        <li>All prices are in Kenyan Shillings (KSh).</li>
                        <li>Any additional work outside the scope will be quoted separately.</li>
                        <li>Please reference quotation number <strong>{quotation.quotation_number}</strong> in all correspondence.</li>
                        <li>For project-based work, a 50% deposit is required before commencement.</li>
                    </ul>
                </div>

                <div class="footer">
                    Thank you for choosing FixKraft Digital.<br>
                    📧 info@fixkraftdigital.com &nbsp;|&nbsp; 📞 +254 748 929 891
                </div>
            </div>
        </body>
        </html>
        """

        # --- Create email with HTML and plain text fallback ---
        subject = f"Your Quotation from FixKraft Digital - {quotation.quotation_number}"
        plain_text = strip_tags(html_content)  # fallback for email clients that don't support HTML

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[client.email],
        )
        email.attach_alternative(html_content, "text/html")  # attach HTML version
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
    