from collections import Counter
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Projects
from inquiry.models import Inquiry
from clients.models import Client
from quotation.models import Quotation
from payment.models import Payment
from django.db.models import Count, Sum

@api_view(['GET'])
def dashboard_stats(request):
    total_projects = Projects.objects.count()
    total_inquiries = Inquiry.objects.count()
    total_clients = Client.objects.count()
    total_quotations = Quotation.objects.count()
    pending_quotations = Quotation.objects.filter(status='pending').count()
    total_payments = Payment.objects.count()

    # dynamic percentage calsulation in admin dashboard
    now = timezone.now()
    last_7_days = now - timedelta(days=7)
    previous_7_days = last_7_days - timedelta(days=7)

    # Current week visitors (last 7 days)
    curr_week_inquiries = Inquiry.objects.filter(created_at__gte=last_7_days)
    visitors_data = [0]*7
    for i in curr_week_inquiries:
        visitors_data[i.created_at.weekday()] += 1

    # Previous week total visitors
    prev_week_inquiries = Inquiry.objects.filter(created_at__gte=previous_7_days, created_at__lt=last_7_days)
    prev_total = prev_week_inquiries.count()
    curr_total = curr_week_inquiries.count()
    if prev_total > 0:
        percent_change = ((curr_total - prev_total) / prev_total) * 100
    else:
        percent_change = 100 if curr_total > 0 else 0
    percent_change = round(percent_change, 1)

    # weekly visitors (based on inquiry creation dates)
    last_7_days = timezone.now() - timedelta(days=7)
    inquiries_last_week = Inquiry.objects.filter(created_at__gte=last_7_days)
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    visitors_data = [0]*7
    for inquiry in inquiries_last_week:
        visitors_data[inquiry.created_at.weekday()] += 1

    # Service distribution - split comma-separated services
    service_counter = Counter()
    for inquiry in Inquiry.objects.all():
        if inquiry.service:
            services = [s.strip() for s in inquiry.service.split(',')]
            for svc in services:
                service_counter[svc] += 1

    top_services = service_counter.most_common(5)
    service_labels = [s[0] for s in top_services]
    service_data = [s[1] for s in top_services]

    # Recent projects
    recent_projects = Projects.objects.order_by('-created_at')[:5]
    recent_projects_list = [{'id': p.id, 'title': p.title} for p in recent_projects]

    # Recent activities with timestamp
    recent_inquiries = Inquiry.objects.order_by('-created_at')[:5]
    activities = [{
        'message': f"New inquiry from {i.client.name} - {i.service}",
        'creayed_at': i.created_at.isoformat()
    } for i in recent_inquiries]

    # top_clients
    top_clients = Client.objects.annotate(inquiry_count=Count('inquiries')).order_by('-inquiry_count')[:5]
    top_clients_data = [{'name': c.name, 'count': c.inquiry_count} for c in top_clients]

    # recent_quotations
    recent_quotations = Quotation.objects.select_related('inquiry__client').order_by('-created_at')[:5]
    recent_quotations_list = [{
        'number': q.quotation_number,
        'client': q.inquiry.client.name,
        'amount': float(q.amount),
        'status': q.status,
    } for q in recent_quotations]

    # pending_total
    pending_total = Quotation.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0

    return Response({
        'stats': {
            'projects': total_projects,
            'inquiries': total_inquiries,
            'clients': total_clients,
            'quotations': total_quotations,
            'pending_quotations': pending_quotations,
            'payments': total_payments,
        },
        'visitors': visitors_data,
        'visitors_trend': percent_change,
        'service_labels': service_labels,
        'service_data': service_data,
        'recent_projects': recent_projects_list,
        'activities': activities,
        'top_clients': top_clients_data,
        'recent_quotations': recent_quotations_list
    })
 