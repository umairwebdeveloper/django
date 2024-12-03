from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from app.utils import send_email
from .models import UserProfile, Transaction, PhoneNumber
from django.contrib.auth.models import User
from django.db import transaction



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
    """
    Sends an email to the user when their transaction is approved,
    avoiding signal-triggered save loops using a transaction.atomic block.
    """
    if created or not instance.approved or instance.email_sent:
        # Skip if the instance is newly created, not approved, or already emailed
        return
    
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

    # Send email and update email_sent field atomically
    try:
        with transaction.atomic():
            send_email(subject, recipient_list, template_path, context)
            instance.email_sent = True
            instance.save(update_fields=['email_sent'])
    except Exception as e:
        # Log the error or handle it as required
        print(f"Failed to send email: {e}")
        
        
@receiver(post_save, sender=User)
def create_or_update_user_phone_number(sender, instance, created, **kwargs):
    if created:
        PhoneNumber.objects.create(user=instance)
    instance.phone_number.save()