from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status

from .models import Inquiry
from .serializers import InquirySerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages

from django.utils.crypto import get_random_string

from .questionnaire_config import QUESTIONNAIRE_CONFIG

from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def requirements_api(request, token):
    inquiry = get_object_or_404(Inquiry, questionnaire_token=token)

    if request.method == 'GET':
        if inquiry.questionnaire_completed:
            return Response({'detail': 'Questionnaire already completed.'}, status=400)
        
        selected_services = [s.strip() for s in inquiry.service.split(',') if s.strip()]
        selected_services = [s for s in selected_services if s in QUESTIONNAIRE_CONFIG]

        # Build questions list
        questions = []
        for service in selected_services:
            questions.extend(QUESTIONNAIRE_CONFIG.get(service, []))

        if not questions:
            questions = [{
                "id": "general_description",
                "label": "Please describe your project in detail.",
                "type": "textarea",
                "required": True
            }]

        return Response({'questions': questions})
    elif request.method == 'POST':
        if inquiry.questionnaire_completed:
            return Response({'detail': 'Questionnaire already completed.'}, status=400)
        
        answers = request.data.get('answers', {})
        inquiry.questionnaire_answers = answers
        inquiry.questionnaire_completed = True
        inquiry.save()

        # Notify admin
        send_mail(
            subject=f"Questionnaire Completed - Inquiry #{inquiry.id}",
            message=f"Client {inquiry.client.name} has completed the requirements questionnaire.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['info@fixkraftdigital.co.ke'],
            fail_silently=True
        )

        return Response({'detail': 'Questionnaire submitted successfully.'}, status=200)

def requirements_questionnaire(request, token):
    inquiry = get_object_or_404(Inquiry, questionnaire_token=token)

    if inquiry.questionnaire_completed:
        messages.info(request, "You have already completed this questionnaire.")
        return redirect('/contact/success')
    
    # Get selected services from the inquiry
    selected_services = [s.strip() for s in inquiry.service.split(',') if s.strip()]
    selected_services = [s for s in selected_services if s in QUESTIONNAIRE_CONFIG]

    # Build the combined question list
    questions = []
    for service in selected_services:
        for q in QUESTIONNAIRE_CONFIG.get(service, []):
            questions.append(q)

    # If no questions found (or no services selected), use a fallback
    if not questions:
        questions = [
            {
                "id": "general_description",
                "label": "Please describe your project in detail.",
                "type": "textarea",
                "required": True
            }
        ]

    if request.method == 'POST':
        answers = {}
        for q in questions:
            qid = q['id']
            value = request.POST.get(qid, '')
            if q.get('required', False) and not value:
                messages.error(request, f"Please answer: {q['label']}")
                return render(request, 'inquiry/requirements_questionnaire.html', {
                    'inquiry': inquiry,
                    'questions': questions,
                    'answers': request.POST,
                    'token': token
                })
            answers[qid] = value

        # Save answers to JSONField
        inquiry.questionnaire_answers = answers
        inquiry.questionnaire_completed = True
        inquiry.save()

        # send notification to admin
        send_mail(
            subject=f"Questionnaire Completed - Inquiry #{inquiry.id}",
            message=f"Client {inquiry.client.name} has completed the requirements questionnaire.\n\nYou can view the answers in the admin panel.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['info@fixkraftdigital.co.ke'],
            fail_silently=True,
        )

        messages.success(request, "Thank you! Your requirements have been received.")
        return redirect('/contact/success')
    return render(request, 'inquiry/requirements_questionnaire.html', {
        'inquiry': inquiry,
        'questions': questions,
        'token': token,
    })

class InquiryViewSet(viewsets.ModelViewSet):
    
    queryset = Inquiry.objects.all().order_by('-created_at')

    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        # 1. Save the inquiry
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Generate token and save
        inquiry = serializer.instance
        token = get_random_string(length=32)
        inquiry.questionnaire_token = token
        inquiry.save()

        # 2. Get validated data
        data = serializer.validated_data
        name = request.data.get('name')
        email = request.data.get('email')
        phone = data.get('phone', 'Not provided')
        message = data.get('message')

        # 3. Send email to admin
        admin_subject = f"New Inquiry from {name}"
        admin_message = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message: {message}"
        )
        try:
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['info@fixkraftdigital.co.ke'],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error (optional)
            print(f"Admin email failed: {e}")

        # 4. Send auto-reply to the user with questionnaire link (optional)
        questionnaire_link = f"{settings.FRONTEND_URL}/requirements/{token}"
        user_subject = "Thank you for contacting FixKraft Digital"
        user_message = (
            f"Dear {name},\n\n"
            "Thank you for reaching out to FixKRaft Digital.\n\n"
            "To help us understand your project better, please complete the requirements questionnaire using the link below:\n\n"
            f"{questionnaire_link}\n\n"
            "This will help us prepare an accurate quotation tailored to your needs.\n\n"
            "Best regards,\nFixKraft Digital Team"
        )
        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True
        )

        # Return the created data
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        # Count inquiries with status 'new'
        count = self.get_queryset().filter(status='new').count()
        return Response({'count': count})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_inquiries(self, request):
        # get client linked to the logged-in user
        try:
            client = request.user.client
        except AttributeError:
            return Response({"detail": "Client profile not found."}, status=404)
        
        inquiries = self.get_queryset().filter(client=client)
        serializer = self.get_serializer(inquiries, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        inquiry = self.get_object()
        inquiry.status = 'read'
        inquiry.save()
        return Response({'status': 'read'})
