from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from sesame.utils import get_token
from django.core.mail import send_mail


# Create your models here.
class Client(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lead', 'Lead'),
        ('churned', 'Churned')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(
        max_length=255
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='lead'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

@receiver(post_save, sender=Client)
def create_user_for_client(sender, instance, created, **kwargs):
    if created and not instance.user:
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=None
            )
        instance.user = user
        instance.save()

        # Send magic link in production (or always, but ensure FRONTEND_URL is set)
        if not settings.DEBUG:
            token = get_token(user)
            magic_link = f"{settings.FRONTEND_URL}/auth/callback?token={token}"
            send_mail(
                'Your account is ready',
                f'Click the link to view your inquiries: {magic_link}',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                # prevent crashing if email fails, by failing silently
                fail_silently=True,
            )
        