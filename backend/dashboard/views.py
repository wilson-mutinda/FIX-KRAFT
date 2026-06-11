from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from projects.models import Projects
from inquiry.models import Inquiry
from clients.models import Client
from quotation.models import Quotation
from payment.models import Payment
from Category.models import MediaCategory
from mediahub.models import Mediahub

# Create your views here.
@api_view(['GET'])
def dashboard_stats(request):
    total_projects = Projects.objects.count()
    total_inquiries = Inquiry.objects.count()
    total_clients = Client.objects.count()
    total_quotations = Quotation.objects.count()
    pending_quotations = Quotation.objects.count()
    total_payments = Payment.objects.count()

    # Weekly visitors (if there is a Visitor model, else derive from inquiry creation dates)
    last_7_days = timezone.now() - timedelta(days=7)
    inquiries_last_week = Inquiry.objects.filter(created_at__gte=last_7_days)

    # Group by day of week (Monday=0, Sunday=6)
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    visitors_data = [0]*7
    for inquiry in inquiries_last_week:
        weekday = inquiry.created_at.weekday()
        visitors_data[weekday] += 1

    # Service distribution from inquiries (group by service field)
    service_dist = Inquiry.objects.values('service').annotate(count=Count('id')).order_by('-count')[:5]
    service_labels = [item['service'][:20] for item in service_dist]
    service_counts = [item['count'] for item in service_dist]

    # Recent Projects (last 5)
    recent_projects = Projects.objects.order_by('-created-by')[:5]
    recent_projects_list = [{'id': p.id, 'title': p.title} for p in recent_projects]

    # Recent activities (last 5 actions - can be derived from model changes; for simplicity, use recent inquiries)
    recent_inquiries = Inquiry.objects.order_by('-created_at')[:5]
    activities = [f"New inquiry from {i.client.name} - {i.service}" for i in recent_inquiries]

    return Response({
        'stats': {
            'projects': total_projects,
            'inquiries': total_inquiries,
            'clients': total_clients,
            'quotations': total_quotations,
            'pending_quotations': pending_quotations,
            'payments': total_payments
        },
        'visitors': visitors_data,
        'service_labels': service_labels,
        'service_data': service_counts,
        'recent_projects': recent_projects_list,
        'activities': activities
    })
