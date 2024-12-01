# admin.py
from django.conf import settings
from django.contrib import admin
from .models import UserProfile
from django.utils.html import format_html

class ImageAdmin(admin.ModelAdmin):
    def profile_image_tag(self, obj):
        if obj.profile_image and obj.profile_image.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.profile_image.url))
        return "No Image"

    def id_card_front_tag(self, obj):
        if obj.id_card_front and obj.id_card_front.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.id_card_front.url))
        return "No Image"
    
    def id_card_back_tag(self, obj):
        if obj.id_card_back and obj.id_card_back.url:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.id_card_back.url))
        return "No Image"
    
    profile_image_tag.short_description = 'Pofile Image'
    id_card_front_tag.short_description = 'ID Card Front'
    id_card_back_tag.short_description = 'ID Card Back'
    list_display = ['user', 'status', 'created_at', 'profile_image_tag', 'id_card_front_tag', 'id_card_back_tag']
    list_editable = ['status']
    readonly_fields = ['profile_image_tag', 'id_card_front_tag', 'id_card_back_tag']

admin.site.register(UserProfile, ImageAdmin)


admin.site.site_header = "Keysavvy Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Keysavvy Admin Dashboard"

from django.contrib import admin
from django.core.mail import send_mail
from .models import Vehicle, Transaction

admin.site.register(Vehicle)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'vehicle', 'user', 'link', 'email_sent', 'created_at')
    actions = ['generate_links_and_send_emails']
    readonly_fields = ('link', 'transaction_id')  # Make the link field read-only

    def generate_links_and_send_emails(self, request, queryset):
        for transaction in queryset:
            if not transaction.email_sent:
                transaction.save()  # Ensure link is generated
                # Send email to user
                send_mail(
                    subject="Your Vehicle Transaction Link",
                    message=f"Hello {transaction.user.username},\n\n"
                            f"Please use the following link to verify your vehicle:\n"
                            f"{transaction.link}\n\n"
                            f"Vehicle Serial Number: {transaction.vehicle.serial_number}",
                    from_email=f'KeySavvy <{settings.EMAIL_HOST_USER}>',
                    recipient_list=[transaction.user.email],
                )
                transaction.email_sent = True
                transaction.save()
        self.message_user(request, "Emails sent successfully.")
    
    generate_links_and_send_emails.short_description = "Generate Links and Send Emails"


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.urls import reverse

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )
    list_display = ('username', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new user creation
            random_password = get_random_string(12)  # Generate a random password
            obj.username = obj.email
            obj.set_password(random_password)
            obj.generated_password = random_password  # Store it temporarily
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Override the response after adding a user to show the random password.
        """
        random_password = getattr(obj, 'generated_password', None)
        if random_password:
            self.message_user(request, f"User created successfully! The random password is: {random_password}")
        return redirect(reverse('admin:auth_user_changelist'))

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)