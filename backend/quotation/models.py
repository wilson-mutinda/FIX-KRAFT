from django.db import models
from inquiry.models import Inquiry
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Quotation(models.Model):

    inquiry = models.ForeignKey(
        Inquiry,
        on_delete=models.CASCADE
    )

    quotation_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(blank=True)

    valid_until = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # NEW: store line items as JSON
    line_items = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        if not self.quotation_number:
            year = timezone.now().year

            # Find the last quotation number for this year
            last = Quotation.objects.filter(
                quotation_number__startswith=f'FK-{year}-'
            ).order_by('quotation_number').last()

            if last:
                last_num = int(last.quotation_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.quotation_number = f'FK-{year}-{new_num:03d}'

        # Calculate total from line_items
        total = sum(item.get('price', 0) for item in self.line_items)
        self.amount = total
        
        super().save(*args, **kwargs)
