from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from sesame.utils import get_token
from clients.models import Client

@api_view(['POST'])
def request_magic_link(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=400)
    
    try:
        client = Client.objects.get(email=email)
    except Client.DoesNotExist:
        # Don't reveal that the email doesn't exist (security)
        return Response({'message': 'If the email exists, we sent a magic link.'}, status=200)
    
    # Generate token
    token = get_token(client.user)

    # Build magic link
    magic_link = f"{settings.FRONTEND_URL}/auth/magic/?token={token}"

    # send_email
    send_mail(
        subject='FixKraft Digital Client Portal Login Link',
        message=f'Click the link below to login to your client portal:\n\n{magic_link}\n\nThis link expires in 15 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )

    return Response({'message': 'Magic link sent to your email!'})
