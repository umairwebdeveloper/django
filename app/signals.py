from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from app.utils import send_email
from .models import UserProfile, Transaction


@receiver(post_save, sender=UserProfile)
def send_status_update_email(sender, instance, created, **kwargs):
    # Check if the status has changed
    if not created and instance.status and instance.status != 'pending':  # Status is updated from the default
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

@receiver(post_save, sender=Transaction)
def send_transaction_approval_email(sender, instance, created, **kwargs):
    # Check if the transaction is approved and it's not a new instance
    if not created and instance.approved:
        user = instance.user
        subject = "Derek accepted your deal"
        recipient_list = [user.email]
        template_path = 'emails/verified_transaction.html'

        # Render email template
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'approved': instance.approved,
        }
        send_email(subject,recipient_list,template_path,context)
        # Update the email_sent field
        instance.email_sent = True
        instance.save(update_fields=['email_sent'])  # Save only the email_sent field