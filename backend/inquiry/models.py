from django.db import models
from clients.models import Client

# Create your models here.

class Inquiry(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('quoted', 'Quoted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    service = models.CharField(
        max_length=255
    )

    budget = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    message = models.TextField()

    quotation_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.client.name} - {self.service}"
