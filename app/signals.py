from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile


@receiver(post_save, sender=UserProfile)
def send_status_update_email(sender, instance, **kwargs):
    # Check if the status has changed
    if instance.status and instance.status != 'pending':  # Status is updated from the default
        user = instance.user
        subject = "Profile Status Update"
        recipient_list = [user.email]

        # Render email template
        context = {
            'user_name': user.username,
            'status': instance.status,
        }
        message = render_to_string('emails/status_update_email.html', context)

        # Send email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email.content_subtype = 'html'
        email.send()
