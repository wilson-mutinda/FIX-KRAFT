from django.db import models

from projects.models import Projects

# Create your models here.
class Payment(models.Model):

    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=100
    )

    transaction_id = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    